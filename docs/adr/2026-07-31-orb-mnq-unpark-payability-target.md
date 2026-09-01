# ADR 2026-07-31 — ORB-MNQ-1 unparked to active research, with a payable-Tradeify-leg target

⚠ **Addendum 2026-07-31b's K_eff/floor-0.98/"AT the Cap" math for a new MNQ seed is SUPERSEDED —
see [`docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md`](2026-08-04-family-k-bank-disclosure-not-gate.md).**
Under current doctrine, `K_eff = K_intrinsic` only (`K_banked` is disclosure-only, not gating); a
new `K_intrinsic=1` MNQ seed screens at floor **0.65**, not 0.98/AT-the-Cap. The unpark decision and
trigger-table supersession recorded in this file's header are unaffected by this note — see
Addendum 2026-08-29 below for full detail, including why the raw MNQ bank count named below (2) is
itself doubly stale as a current figure.

**Status:** `Accepted` — operator GO in chat 2026-07-31 ("Sibling candidate and Unpark / reopen ORB-MNQ as active research"); the two Addendum-2026-07-31b adjudications ruled same day; §7 Phase-2 downstream sync complete; **§7 Phase 3 DONE and §4 T1 discharged `PASS`** same day (Addendum 2026-07-31c); **§4 T2 MEASURED 2026-08-02 — disposition OWED, no trigger declared and no k policy moved** (Addendum 2026-08-02). **⚠ SUPERSEDED IN PART 2026-08-03 — the T2 disposition was ruled, T2 FIRED on the Part A bust reading, ORB-MNQ-1 is re-`PARKED`, and the payable-Tradeify-leg target is recorded FALSIFIED.** §2's unpark decision and §4's trigger table below are **no longer in force** — see [`2026-08-03-orb-mnq-repark-payability-falsified.md`](2026-08-03-orb-mnq-repark-payability-falsified.md). Everything else here — §3 evidence, Addendum 31b's two rulings, Addendum 31c's T1 `PASS`, and Addendum 2026-08-02's measurement — **stands as `Accepted` record and is not retracted.**
**Decision date:** 2026-07-31
**Supersedes:** [`2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md`](2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md) in part — the 2026-07-24 Addendum's `TERMINAL` clause **only as it applies to Candidate B (ORB-MNQ)**. Candidate A (MYM ORC) stays CLOSED, R5/P2 stay FALSIFIED, and the standing c1-execution-quality research interest is unaffected.
**Superseded-by:** none
**Superseded-in-part-by:** [`2026-08-03-orb-mnq-repark-payability-falsified.md`](2026-08-03-orb-mnq-repark-payability-falsified.md) — the **§2 unpark decision**, the **payable-`Tradeify_Select_100K`-leg target**, and the **§4 trigger table** only. T2 was ruled FIRED on the Part A bust reading; ORB-MNQ-1 returns to `PARKED` and the target is recorded FALSIFIED. §3's evidence, Addendum 2026-07-31b (both rulings), Addendum 2026-07-31c (T1 `PASS`), and Addendum 2026-08-02 (T2 measurement) are **retained as `Accepted` record**.
**Retain-until:** none
**Authors:** Cursor (measurement + recorder); operator GO in chat 2026-07-31
**Related:** [`lab/analysis/orb/orb_mnq_2026-07/ADMISSION.md`](../../lab/analysis/orb/orb_mnq_2026-07/ADMISSION.md) (lifecycle admission, unchanged) · [`Q-COMPOSE-1 closure`](../briefs/closures/Q-COMPOSE-1-closure-falsified.md) (kills the book-leg role, not the candidate) · [`2026-07-30-tradeify-native-fade-program-design.md`](../superpowers/specs/2026-07-30-tradeify-native-fade-program-design.md) (payability arithmetic this ADR corrects for ORB's shape)
**Layer:** research-authorization status. **No locked parameter, allocation, `dd_protection` constant, `ACTIVE_FIRM`, rail, `LEG_MAP`, or Pine construct is touched.**

---

## §0 — Rule 0 reads (production source, verified this session at `308fd62`)

- [`docs/adr/2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md`](2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md) §Addendum 2026-07-24 — the clause this ADR partially supersedes. Verbatim: *"MYM and MNQ are terminal, and we are still open to improving execution (better fills and exits)"*; and *"a reconstruction re-open requires a fresh operator GO + pre-registration, not a revert of this addendum."*
- [`lab/analysis/orb/orb_mnq_2026-07/ADMISSION.md`](../../lab/analysis/orb/orb_mnq_2026-07/ADMISSION.md) — lifecycle `CANDIDATE @ 1.00×` with four standing caveats; **no `core/lifecycle.py` write**.
- [`docs/briefs/pre-registration/2026-07-16-orb-nas100-mnq-reconstruction-preregistration.md`](../briefs/pre-registration/2026-07-16-orb-nas100-mnq-reconstruction-preregistration.md) §2/§3/§5 — frozen construct, `K_intrinsic=1 / K_eff=2`, DSR floor ladder (K=1→0.65 · 2→0.85 · 3→0.98 · 4→1.06 FAIL), and the forbidden-moves list (no conditioning gates).
- [`core/strategies/orb/orb_mnq_v0_2_CANDIDATE.md`](../../core/strategies/orb/orb_mnq_v0_2_CANDIDATE.md) — v0.2 D1–D5 venue-conformance amendment; D5 pins full-session `sessOpen`/`sessClose` as constants (landed `66c2a14`, PR #574).
- [`lab/analysis/orb/orb_mnq_2026-07/RESULTS_v02_clock_kgrid.md`](../../lab/analysis/orb/orb_mnq_2026-07/RESULTS_v02_clock_kgrid.md) — the TV-export scorecard on the **defective 15:30 clock**; its §3 forbids freezing a k policy until a 16:00 re-export is scored.
- [`lab/analysis/orb/orb_mnq_2026-07/RESULTS_stage7.md`](../../lab/analysis/orb/orb_mnq_2026-07/RESULTS_stage7.md) — full-window Tradeify DSR **FAIL** at $0.91/side; 2021+ passes all four FRIENDLY firms to 3 ticks.
- [`docs/briefs/closures/Q-COMPOSE-1-closure-falsified.md`](../briefs/closures/Q-COMPOSE-1-closure-falsified.md) §Dispositions — *"A failed composed candidate closes; it does not iterate weight (§5)."*
- [`docs/notes/2026-07-24-tradeify-rulepin-verification.md`](../notes/2026-07-24-tradeify-rulepin-verification.md) — pin 1 **VERIFIED**: *"Winning Day Threshold: … 100K Account: $200 minimum profit per day."*
- [`STATE.md`](../../STATE.md) pointer log 2026-07-30 — Tradeify enforces the drawdown breach **in real time**, so every bust figure in the repo is a **lower bound**.

---

## §1 — Context

ORB-MNQ-1 was admitted lifecycle `CANDIDATE @ 1.00×` on 2026-07-16 after clearing Stages 2/5/6/7, then **PARKED** by operator directive #6 on 2026-07-23, and swept into the 2026-07-24 addendum's `TERMINAL` ruling on the venue-native reconstruction lane. That addendum set its own reopen condition explicitly: **a fresh operator GO plus a pre-registration** — not a revert.

Two things changed on 2026-07-31. First, the operator gave that GO in chat, naming a concrete target (a payable standalone Tradeify leg) and a second track (a sibling candidate). Second, and before any brief was authored, the cheap falsifier was run PARENT-side per the standing session-discipline rule — and it materially changed the picture the reopen would otherwise have been written against.

The falsifier ([`RESULTS_v02_native_clock.md`](../../lab/analysis/orb_mnq_2026-07/RESULTS_v02_native_clock.md)) exploited a dependency the TV-export path does not have: `orb_lib.CLOSE_TOD_US` is 15:45, so the **native harness has always run the correct 16:00 clock**, and the defective 15:30 clock is reproducible by setting `close_tod = 15:15`. That made both clocks measurable offline today, with no TradingView interaction — which mattered, because the owed operator TV paste collides with the B7 Stage-1 window that voids on any TV UI interaction.

**Decision driver (one sentence):** the 07-24 addendum's own reopen condition is now satisfiable, and the Phase-0 measurement has already run — so the reopen can be recorded against measured numbers instead of an intention, which is the only form in which it is worth recording.

---

## §2 — Decision

**ORB-MNQ-1 is unparked to ACTIVE RESEARCH under the prop-portfolio program, with the research target: a *payable* standalone `Tradeify_Select_100K` leg.**

**Effective:** immediately upon acceptance.
**Scope:** research-authorization status of Candidate B (ORB-MNQ) only.

What this decision does **not** do — each stated because each is a live temptation:

| Unchanged | Status after this ADR |
|---|---|
| Frozen construct (parameter axis) | **LOCKED**, per the 2026-07-16 pre-reg §2/§5. OR=2×15m, both-sides touch-fill, stop=opposite OR extreme, flat at session close, one trade/day, no gates. |
| Lifecycle standing | `CANDIDATE @ 1.00×`, unchanged. No `core/lifecycle.py` write. |
| Book-leg role | **Still FALSIFIED** by Q-COMPOSE-1. This ADR does not re-open composition into the c1 book. |
| Rail integration / account registration / live spend | **Still separately gated.** No arming, no `LEG_MAP` entry, $0. |
| Candidate A (MYM ORC) | **Still CLOSED.** R5/P2 still FALSIFIED. |
| c1 execution-quality research interest | Unaffected and still standing. |
| D5 (16:00 clock pin) | **Correct and retained** — see §5 first bullet. |

---

## §3 — Evidence quality (what the Phase-0 falsifier actually established)

**Method validated.** The native harness reproduces the published Stage-2 anchor exactly: full-window net meanR **+0.0668** on n=1,846 and 2021+ **+0.0894** on n=1,420, both matching [`RESULTS.md`](../../lab/analysis/orb_mnq_2026-07/RESULTS.md) to four decimals. Trade-day mapping is asserted elementwise against the engine's own `range` array before any dollar conversion.

**Finding 1 — the D5 conformance fix costs edge.** Same construct, same data, same Tradeify economics; only the session-end clock differs:

| Clock | n | net meanR | net $ (k=1) | WR | stopped |
|---|---:|---:|---:|---:|---:|
| Correct — exit 16:00 (v0.2 contract) | 1,846 | **+0.0626** | **$17,780** | 46.37% | 38.0% |
| Defective — exit 15:30 (pre-D5 export) | 1,841 | +0.0778 | $23,738 | 47.58% | 35.9% |

61.2% of common days differ; total delta **−$5,832** (−25% of net), mean **−$3.17/day**. The final 30 minutes of RTH are a net-negative P&L term for this construct, and they convert +2.1pp more days into stop-outs. **The published k-grid was flattering, not merely mis-clocked** — it scored a construct that exits before a loss-making half hour. The owed re-export will therefore return **worse** than the 07-30 panel; that is expected, not a defect.

**Finding 2 — k does not resolve payability, but ORB is not structurally unpayable.** This is the substantive correction. The fade-program spec's *"one trade/day is structurally unpayable"* was derived for a high-WR / low-R:R construct whose best possible day is $107–140 — it can never reach $200. ORB has the opposite shape: held-to-close winners average **$181.53 at a 74.8% win rate** (recent 2y, k=1). Measured payable-day rates on the correct clock:

| Window | n | k=1 | k=2 | k=3 |
|---|--:|--:|--:|--:|
| FULL 2019-05+ | 1,846 | 17.8% | 31.4% | 36.0% |
| 2021+ | 1,420 | 20.8% | 34.9% | 38.6% |
| recent ~2y | 502 | 23.3% | 36.9% | 40.6% |

The constraint is **cadence, not impossibility**. The k ∈ {1,2,3} safe band is confirmed on the correct clock (worst day −$784 × k against the $3,000 trail; k ≥ 4 single-day bustable). The price of buying cadence with k is **trail episodes**: k=1→3 lifts payable days 17.8%→36.0% but takes episodes 3→12 with only $649 of single-day headroom left. k=2 is the balanced cell (31.4%, $1,432, 8 episodes).

**Honest limits.** Trail episodes are an **EOD proxy and therefore a lower bound** — Tradeify enforces breach in real time (§0). Full-window Tradeify DSR already FAILED at $0.91/side; only 2021+ carries cushion. The panel ends 2026-07-15 against the export's 2026-07-30. Engine ≠ Pine (96.9% per-trade parity, documented).

---

## §4 — Falsifier (revert trigger)

**H (the hypothesis this reopen stands or falls on, binary):** *there exists an admissible
configuration of the frozen ORB construct — a contract count `k ∈ {1,2,3}`, optionally paired with
one admitted sibling mechanism — that is simultaneously (a) **payable** on a `Tradeify_Select_100K`
funded account at the verified $200 winning-day threshold, and (b) **survivable**, i.e. retains
positive single-day headroom against the $3,000 trail under intraday-honest bust accounting.*

The hypothesis is **RESOLVED** if such a cell is admitted on a pre-registered gate before
2026-11-08; **FALSIFIED** if any trigger below fires; **AMBIGUOUS** if the measurement is blocked
by an unresolved engine/Pine disagreement (T1), which is a halt condition, not a verdict.

**If any trigger below fires, ORB-MNQ-1 returns to `PARKED` by a superseding ADR and the payability target is recorded FALSIFIED.**

| # | Trigger | Threshold | Action |
|---|---|---|---|
| T1 | Post-D5 16:00 TV re-export contradicts the native-harness clock-delta prediction | Full-session cohort P&L does **not** move in the predicted direction (down) at an order of magnitude consistent with −$3.17/day | **Halt.** Engine/Pine disagreement is a defect, not a result — investigate before any further k or sibling work |
| T2 | Intraday-honest bust accounting (once the 07-30 follow-on `intraday_low=` limb lands) re-scores the deployed k | k=2 single-day bust exceeds the frozen 3.0% ceiling | k policy capped at k=1; payability target re-scoped by amending ADR |
| T3 | Program §4 hard date reached with no admitted payable configuration | **2026-11-08**, no `(k, variant)` cell admitted on a pre-registered gate | Re-park ORB-MNQ-1; record the payability target FALSIFIED |
| T4 | Sibling track exhausts without an admissible seed | Fade-program Stage-0/1 kill **or** operator declines both residual routes in Addendum 2026-07-31b | ORB-MNQ-1 stays unparked at k-policy scope only; no harvest-lane MNQ sibling licensed without new mechanism evidence **and** an adjudicated K-bank that leaves Cap room |

**Revert action:** author a superseding ADR (full or in-part per the edge rules); never silently edit this ADR's decision text.
**Trigger check schedule:** T1 on the next TV re-export; T2 when the `intraday_low=` limb lands; T3 at the 2026-08-08 checkpoint and again before 2026-11-08; T4 at sibling closure.

---

## §5 — Forbidden moves (under this ADR)

- **Adopting the 15:30 exit because it backtests better.** Genuinely tempting — it is worth **+$5,832** on the full window, and the "defect" is more profitable than the fix. Ruled out: choosing an exit time on backtest P&L is exit-time tuning, it sits inside the space already pre-killed in [`RESULTS_tv_export_realism.md`](../../lab/analysis/orb/orb_mnq_2026-07/RESULTS_tv_export_realism.md) §2b/2c, and it would constitute a new candidate at `K_eff = 3` (DSR floor **0.98**) which the construct's own full-window annSR of **0.890** does not clear. **D5 stands.** The edge loss is the price of conformance, recorded rather than harvested.
- **Freezing any k policy on the defective 15:30 panel**, or quoting `RESULTS_v02_clock_kgrid.md` dollar paths as current. They are superseded by the correct-clock table in §3.
- **Re-adding conditioning gates to ORB-MNQ itself.** Four attempts (overnight-path / gap / GEX / T10Y3M) and two selection cuts (Friday, DOW) are FALSIFIED and registered; pre-reg §5 forbids it outright, and any gate makes it a new candidate at floor 0.98.
- **Iterating the Q-COMPOSE-1 book weight.** That closure's §5 forbids weight iteration explicitly; a failed composed candidate closes.
- **Treating the EOD-proxy trail-episode counts as the bust number.** They are lower bounds (§0, §3). Sizing to them is the exact error the 07-30 primary-source read exposed.
- **Re-opening Candidate A (MYM ORC) or R5/P2 under cover of this ADR.** The in-part supersession is scoped to Candidate B alone.
- **Loosening any §4 trigger without a superseding ADR** — Known Trap #12.

---

## §6 — Consequences

**Verdict carried into this section:** §4's hypothesis H is **open** — neither RESOLVED nor
FALSIFIED today. This ADR authorizes the work that decides it; it does not pre-judge it, and the
§3 evidence is deliberately reported in the direction that makes FALSIFIED more likely, not less.

**Positive:**
- The reopen is recorded against **measured** numbers, satisfying the 07-24 addendum's own condition properly rather than by assertion.
- A real defect in the published record is corrected before it propagates: the k-grid's dollar paths were flattering by 25% of net, and anyone comparing the re-export to it would have misread the drop as a data or Pine fault.
- k geometry is now readable **without** operator TV hours, decoupling ORB research from the B7 critical path.
- The fade-program's payability arithmetic gains a scoped counter-example (shape-dependence), which is reusable for any future low-WR/high-R candidate.

**Negative (real cost):**
- ORB-MNQ is measurably **weaker** than the published record implied at the correct clock (+0.0626 vs +0.0778 meanR).
- Reopening consumes research attention while the prop-portfolio §4 falsifier is undischarged with a 2026-11-08 hard date.
- A harvest-lane sibling on MNQ is **at or over the Cap** (see Addendum 2026-07-31b) — the sibling track cannot be a `register_search` campaign as originally framed.

**Risks:**
- **Payability may be unreachable at any admissible k.** k=3 buys cadence but leaves $649 of headroom against a bust measure that is a known lower bound. Mitigation: T2.
- **Sibling harvest-lane is Stage-0 dead as framed** (Addendum 2026-07-31b). Mitigation: route under the existing K=0 fade program, or drop; T4 updated accordingly.

**Downstream artifacts needing update (gated on acceptance — see §7):**
- [`CLAUDE.md`](../../CLAUDE.md) §Live-execution posture — the pointer line currently reads ORB-MNQ "admitted then PARKED"; add one line, never a retelling.
- [`STATE.md`](../../STATE.md) — pointer log entry; carry into the operator queue only if it earns operator hours (it does not today).
- [`docs/adr/2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md`](2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md) — gains `Superseded-in-part-by` for this slug.
- [`lab/analysis/orb/orb_mnq_2026-07/RESULTS_v02_clock_kgrid.md`](../../lab/analysis/orb/orb_mnq_2026-07/RESULTS_v02_clock_kgrid.md) — add a pointer to the correct-clock supersession.
- [`docs/adr/INDEX.md`](INDEX.md) — regenerate.
- [`docs/SESSIONS.md`](../SESSIONS.md) — session entry.

---

## §7 — Implementation plan

- **Phase 0** — ✅ **DONE 2026-07-31.** Cheap falsifier run PARENT-side before authoring ([`RESULTS_v02_native_clock.md`](../../lab/analysis/orb_mnq_2026-07/RESULTS_v02_native_clock.md), harness `run_v02_native_clock_kgrid.py`). $0.00, no pull, no K spend.
- **Phase 1** — ✅ **DONE 2026-07-31 (Stage-0 kill of the harvest-lane sibling as framed).** See Addendum 2026-07-31b. Residual sibling work is operator-owned (K-bank adjudication + fade-program route), **not** a gate on accepting this reopen.
- **Phase 2** — ✅ **DONE 2026-07-31.** Downstream pointer sync per §6; reverse `Superseded-in-part-by` edge added to the 2026-07-16 ADR; `docs/adr/INDEX.md` regenerated; SESSIONS entry appended.
- **Phase 3** — ✅ **DONE 2026-07-31 (same day).** Operator pasted the reconstructed D5 source (`e3b37857…`) and re-exported after the B7 window closed at 13:00 ET; export `…_2026-07-31_6ce33.csv` prints full-session EOD at **16:00** on 274 fills. **T1 evaluated: PASS** (§Addendum 2026-07-31c). Scorecard regenerated on the correct clock — [`RESULTS_v02_clock_kgrid.md`](../../lab/analysis/orb/orb_mnq_2026-07/RESULTS_v02_clock_kgrid.md).
  - *Blocker found and cleared same day:* restoring the gitignored `.pine` at wrap-up exposed that the D5 source pinned as the active working edition (`bad8068d…`) exists on no disk and in no transcript — `.pine` is gitignored and the pinning commit `66c2a14` (PR #574) was authored by a **Cursor cloud agent** on an ephemeral VM, so the bytes died with it. A recurrence of `fd91f37b…` one block above it in the same manifest. The only survivor was the **pre-D5** `f60104eb…`, whose session bounds are chart-overridable `input.int`s — precisely the defect class D5 closed, and the mechanism behind the 15:30 export.
  - *Resolution (operator ruling):* D5 **reconstructed** from `f60104eb…` and re-pinned as `e3b37857…` — the four full-session bounds become constants; early-close bounds stay inputs (calendar, not clock). Values are byte-identical to the pre-D5 defaults (9/30/16/0), so **no parameter or construct moved**; only chart-overridability is removed. Reproducible via [`reconstruct_d5.py`](../../lab/analysis/orb_mnq_2026-07/reconstruct_d5.py) (asserts the base hash first); `pine_check.py` clean. This is a **reconstruction, not a recovery** — it does not reproduce `bad8068d…` byte-for-byte and claims not to.
  - *§3 evidence unaffected:* every number in this ADR comes from the native Python harness, which implements the clock itself and never reads the `.pine`.
  - *Guard added:* `scripts/check_pine_manifest.py --check-pin-provenance` refuses a gitignored pin added from a checkout that cannot persist the bytes. Regression-tested against `66c2a14` itself — it fires on the real incident. **Coverage is partial and knowingly so:** the pre-commit limb cannot see the case it was written for (a fresh cloud-agent clone has no hooks), and the PR limb — the only one that could catch a pin *before* the bytes are lost — is **inert while GitHub Actions is disabled repo-wide** (verified 2026-07-31: `actions/permissions {"enabled":false}`, no run since 2026-07-16). The live limb is detection-on-arrival in `scripts/githooks/post-merge`, which runs on a durable machine but only *after* the bytes are gone. Re-enabling Actions restores the pre-loss gate with no new work, and is deliberately left as an operator decision because it also resumes three workflows that were failing when it was switched off.
- **Phase 4** — ✅ status `Accepted` 2026-07-31 (`check_adr_graph.py` exit 0).

---

## §10 — Audit hooks (runnable)

```bash
# The in-part supersession is scoped to Candidate B only — Candidate A must stay CLOSED
rg -n "MYM ORC|Candidate A" docs/adr/2026-07-31-orb-mnq-unpark-payability-target.md
# Expected: only §2 table + §5 forbidden-move bullet, both asserting it stays CLOSED

# Phase-0 falsifier reproduces (the numbers §3 is written against)
.venv-research/Scripts/python.exe lab/analysis/orb_mnq_2026-07/run_v02_native_clock_kgrid.py
# Expected: cross-check +0.0668 full / +0.0894 2021+; correct-clock net $17,780; delta -$5,832

# The frozen construct was not edited (forbidden-move check)
rg -n "conditioning gate|filter|BE stop|give-back" docs/briefs/pre-registration/2026-07-16-orb-nas100-mnq-reconstruction-preregistration.md
# Expected: only inside §5 forbidden-moves prose, never as an active design element

# D5 still pinned as constants (the fix this ADR declines to un-do)
rg -n "D5|sessClose" core/strategies/orb/orb_mnq_v0_2_CANDIDATE.md
# Expected: full-session open/close described as CONSTANTS, not inputs

# ADR graph integrity
python scripts/check_adr_graph.py
# Expected: exit 0 (A2 reverse-edge skipped while this ADR is Proposed)
```

---

## Addendum 2026-07-31b — sibling Stage-0 disposition (harvest-lane DEAD as framed)

The companion sibling track was researched before any pre-registration was authored (session-discipline cheap-falsifier rule, applied to the intake rather than the construct). Findings, with owners:

### What was checked

- Register / ledger / manifest mechanics (`lab/discovery/register_search.py`; template `discovery_manifests/orb_mnq_intraday_breakout.json`, still `"open"`).
- MNQ family K-bank vs Cap (`docs/methodology/strategy_harvest.md` §1 Req 3; `Q-KBUDGET-1` floor ladder; ST-EH-1 pre-reg's conservative count of the open ORB manifest).
- Dedup surface (`docs/rejected_candidates.md` — the machine `dedup_check` code was **retired 2026-07-11** with Gen-1; dedup is now a prose §0/§1 gate; composite key would return CLEAR for a fade×MNQ, but the **line-411 raised bar** and harvest Reqs bind harder).
- Harvest admission of the catalog seed (`lab/archive/external_sourcing_2026-06-30/catalog.md` §failed-ORB-fade; five requirements in `strategy_harvest.md`).
- Existing fade apparatus (`lab/analysis/c1/tradeify_fade_stage0_2026-07-30/`, ACTIVE, **$0 / K=0 / no mechanism scored**).

### Verdict on the catalog "failed-ORB-fade" as a harvest-lane campaign

| Req | Result | Why |
|---|---|---|
| 1 Economic grounding | **FAIL** | Catalog story is *"trapped breakout traders"* — a preference/behavioral claim. Path 1a no longer admits those (ADR 2026-07-26 §2-A); Path 1b fails all four evidence tests (undated educational HighStrike/TradeAlgo, no multi-decade / multi-cohort / late-replication record). |
| 2 Cohort δ/σ on MNQ | **UNSCREENABLE** | Claimed "~52% WR on SPY" is not a δ/σ, and SPY→MNQ is a cross-instrument transplant (inadmissible). |
| 3 Family K-bank | **AT OR OVER CAP** | Harvest doctrine: MNQ bank = 2 → new K_intrinsic=1 ⇒ **K_eff=3, floor 0.98, at the Cap**. ST-EH-1 conservative convention already counted the still-open ORB manifest ⇒ bank 3 → new seed **K_eff=4, floor 1.06 FAIL**. Req 3 has **no recovery route**. |
| 4 Confirm-power | not computable | Needs the δ/σ Req 2 cannot supply. |
| 5 Cost-law | not computable as declared | MNQ 4× hurdle pinned at ≈3.01 bp/session (`ops/instruments/MNQ.md` N6); fade geometry has a *smaller* stop than ORB, so cost-in-R is adverse vs the parent. |

Sourcing tier is the worst available (rank-6 practitioner blog × Tier-C intraday microstructure / graveyard-watch). The entry is unscreened residue from a sweep that produced **0 admissions**.

**Do not author a harvest-lane pre-registration for this seed.** Writing one would burn operator attention against a known Stage-0 kill.

### Two operator adjudications — BOTH RULED 2026-07-31 (chat)

**Ruling 1 — the open ORB manifest does NOT count toward `K_banked(MNQ)`.** Operator: *"It doesn't count."*

- **`K_banked(MNQ) = 2`** (D5 closed 1 + ST-EH-1's MNQ half 1). A new MNQ seed at `K_intrinsic=1` is therefore **`K_eff = 3`, DSR floor 0.98 — open, but AT the Cap: one such seed only.**
- This **affirms** [`docs/methodology/strategy_harvest.md`](../methodology/strategy_harvest.md) §1 Req 3 as written (2026-07-27) and **supersedes the conservative counting convention** used in [`2026-07-26-st-eh-1-preregistration.md`](../briefs/pre-registration/2026-07-26-st-eh-1-preregistration.md) §DSR-denominator, which counted the open ORB manifest. ST-EH-1's own closed result is unaffected — its denominator was conservative, i.e. it cleared a *higher* bar than required.
- **Doctrine now settled:** a manifest banks K when it **closes**, not while it is open. Standing implication — leaving a manifest open does not reserve Cap room, and closing one does not free it.
- **The Cap is not a budget to spend down casually.** With MNQ at 2, the family has room for exactly one `K_intrinsic=1` campaign before floor(K_eff=4)=1.06 exceeds Cap 1.0 and kills the family permanently (Req 3 has no recovery route). Any proposal to spend that single remaining seat is an operator decision, not an author's.

**Ruling 2 — sibling residual route = (a), scope under the existing fade program.** Operator: *"a"*.

- ORB-complement fade work is routed as a **K=0 Stage-0 δ-extraction under the already-ACTIVE** [`lab/analysis/c1/tradeify_fade_stage0_2026-07-30/`](../../lab/analysis/c1/tradeify_fade_stage0_2026-07-30/) program ($0 spend, K=0, no mechanism scored, MNQ cost pins already held).
- **No `register_search` open, no new discovery manifest, no K spend** is authorized by this routing. The MNQ Cap seat identified in Ruling 1 stays **unspent**.
- The catalog's trapped-trader story is **not** carried across — it failed harvest Req 1 and remains failed. Any mechanism scored under the fade program must satisfy that program's own Stage-0 discipline on its own terms.
- The fade program's two standing operator rulings (roll-window disposition; governing cost-law multiple) are **unchanged and still owed** — this routing does not resolve or bypass them.

### How the 07-24 addendum's "pre-registration" limb is satisfied

The 2026-07-24 addendum requires *"a fresh operator GO + pre-registration"* to reopen. With the sibling campaign dead, that limb is satisfied **by the existing frozen pre-registration**, not by a new one: [`2026-07-16-orb-nas100-mnq-reconstruction-preregistration.md`](../briefs/pre-registration/2026-07-16-orb-nas100-mnq-reconstruction-preregistration.md) remains FROZEN with its §8 GO signed, and it governs the construct this ADR reopens. **This reopen authorizes no new search** — no new manifest, no K spend, no parameter widening — so there is no new search to pre-register. Should any new search be proposed later (including spending the MNQ Cap seat), it requires its own frozen pre-registration at that time.

This addendum does **not** change §2 (ORB-MNQ-1 is still unparked to active research under the payability target). It removes the sibling harvest-lane pre-registration as a gate on accepting this ADR.

---

## Addendum 2026-07-31c — §4 **T1 discharged: PASS**. The re-export confirms the prediction, and is worse than the prediction implied.

Phase 3 closed the same day it unblocked. The operator pasted the reconstructed `e3b37857…` and
re-exported MNQ1! 15m after the B7 Stage-1 window closed at 13:00 ET, satisfying the
outside-a-measurement-window constraint. Export `…_2026-07-31_6ce33.csv`, n=513,
2024-07-30→2026-07-30 — the **same window and trade count** as the pre-D5 panel.

### The clock is fixed

274 full-session EOD fills at **16:00** (was 15:30), 15 half-day at 12:45, **0** elsewhere;
duration identity PASS; commission still $0.61/side Bulenox. D5 holds on a live TV chart, so the
chart-override class it pins shut is closed in practice and not only in source.

### T1: **PASS** — direction and magnitude both as predicted

Full predicted-vs-observed comparison (direction, per-day Δ, total Δ at k=1, share of days moved,
worst/best single-day Δ) — table moved to
[`RESULTS_v02_clock_kgrid.md`](../../lab/analysis/orb/orb_mnq_2026-07/RESULTS_v02_clock_kgrid.md),
the canonical owner. Measured **both** ways and identical to the cent: per-common-day pairing
against the surviving pre-D5 export, and the published-totals fallback. **The early-close control
cohort is byte-stable** — all 18 rows unchanged — so the delta is *attributable* to the session
clock rather than merely coincident with it. That control is what makes this a measurement rather
than a comparison.

T1 therefore does **not** fire. §4's hypothesis H remains **open**; nothing here resolves or
falsifies it, and no k policy is frozen.

### Adverse finding this surfaces (no trigger fires, and it is not read as one)

The corrected panel is worse than §3's percentage prediction implied. Full net/PF/maxDD/RF/days≥$200/
2026-YTD comparison (15:30 published vs 16:00 correct) — see
[`RESULTS_v02_clock_kgrid.md`](../../lab/analysis/orb/orb_mnq_2026-07/RESULTS_v02_clock_kgrid.md),
the canonical owner. Two figures from that table are cited elsewhere in this repo as owned by this
ADR (e.g. [`Q-SESSCONF-1`](../briefs/rnd-pipeline/Q-SESSCONF-1-mnq-session-confluence-longer-hold-scoping.md)):
corrected-clock **RF 0.93** (was 1.52 published) and **2026 YTD net −$2,431**, n=147 (was −$672
published). **RF falls below 1** — max drawdown now exceeds net profit over the window, with net
down *and* drawdown up. **2026 is a material loser, not roughly flat** — this is the regime that
would have to supply the cadence the payability target needs, so it is adverse evidence against H
specifically.

**Recorded, not acted on.** No §4 trigger covers profitability decay on the deployed rung: T1 is
discharged, T2 waits on the `intraday_low=` limb, T3 is the 2026-11-08 hard date, T4 is sibling
closure. Reading RF < 1 as a de facto FALSIFIED would be inventing a trigger after seeing the data —
the mirror image of the loosening §5 forbids. It is carried as the leading input to the **2026-08-08
checkpoint** and to any future k-policy proposal, which must now clear it explicitly.

The k band is **unchanged**: worst day is still −$784, so k ∈ {1,2,3} retain single-day headroom
($2,216 / $1,432 / $649) and k ≥ 4 stays single-day bustable. Trail episodes at k=1/2/3 are
**5 / 10 / 13**, still EOD-proxy lower bounds per §0.

### What is now closed vs still owed

- **Closed:** the clock question, T1, and §7 Phase 3. `RESULTS_v02_clock_kgrid.md` is current — its
  supersession banner self-removed, since the file no longer sits on a defective clock.
- **Still owed, unchanged:** T2's `intraday_low=` limb · the fade program's two rulings · T3 at
  2026-11-08. **Actions remains disabled repo-wide**, so the pin-provenance PR limb stays inert.

---

## Addendum 2026-08-02 — §4 **T2 measured**. The `intraday_low=` limb is fed for the first time; the trigger's two readings disagree, and the intraday correction decides neither. **Disposition owed — not self-taken.**

**Record:** [`RESULTS_t2_intraday_bust.md`](../../lab/analysis/orb/orb_mnq_2026-07/RESULTS_t2_intraday_bust.md) ·
harness [`run_t2_intraday_bust.py`](../../lab/analysis/orb_mnq_2026-07/run_t2_intraday_bust.py) ·
controls [`test_t2_intraday_bust.py`](../../lab/analysis/orb_mnq_2026-07/test_t2_intraday_bust.py) (7 passed).
**$0** — no databento pull, no cost dry-run, no TV export, no K spend, no manifest, nothing armed.
No `core/`, allocation, `dd_protection`, Pine, rail, `LEG_MAP`, or lifecycle touch.

### What was actually missing

`core/mc/simulation.py::simulate_path` gained the opt-in `intraday_low=` argument on 2026-07-30.
**Nothing ever fed it.** `run_seed` builds its bootstrap `path` from daily P&L blocks only, so every
published bust figure in this repo tests the barrier against the *close*. The gap was computational,
not a data-acquisition gap: two pieces were unwritten — a per-day excursion derivation for the ORB
construct, and a **paired** block bootstrap (production `run_seed` cannot carry a second per-day
series, so the same drawn block indices must be applied to both panels). Both are written here.

The derivation is **not** `min(Low)` over the session's bars — that is wrong-signed for shorts (the
adverse extreme is the high) and counts bars before entry and after exit. It is the position's worst
mark: a **stopped** day resolves *at* the opposite OR extreme so its excursion ≡ its realized P&L; a
**held-to-close** day takes the worst post-entry mark, bounded strictly above −range by construction.
15m bars are sufficient and this is not a resolution compromise — an OHLC bar records the actual
traded extreme within it; only the *timestamp* of a crossing is lost, and nothing here depends on it.

### T2's threshold welds two different units, and they disagree

*"k=2 single-day bust exceeds the frozen 3.0% ceiling"* joins a **single-day** quantity to a
**Monte-Carlo rate** ceiling. Both readings, measured — the literal single-day-bust reading is
**NOT met** (0 days reach the $3,000 trail at any k ∈ {1,2,3}; k=2 keeps $1,432 headroom), the
Part-A-bust-MC ceiling reading **IS met** (k=2 intraday-honest 77.01% vs 3.0% — 26× over) — full
table moved to [`RESULTS_t2_intraday_bust.md`](../../lab/analysis/orb/orb_mnq_2026-07/RESULTS_t2_intraday_bust.md).

### The intraday correction is not what fires it

Pre-registered protocol unedited ([survivor-scoring pre-reg](../briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md)):
bust ≤ 3.0% ∧ P(pass) ≥ 50%, Run-2 (consistency 40%), `Tradeify_Select_100K`, horizon 1500, seeds
42/123/2026, **10,000 sims/seed**, inactivity off, `dd_protection` off; 375 Mon-anchored blocks over
1,878 business days. Headline bust via `preflight.summarize_outcomes` (daily+static+**trailing**).

Full k=1/2/3 EOD-arm vs intraday-honest vs P(pass) table — moved to
[`RESULTS_t2_intraday_bust.md`](../../lab/analysis/orb/orb_mnq_2026-07/RESULTS_t2_intraday_bust.md),
the canonical owner (headline cell: k=2 intraday-honest **77.01%**, P(pass) **22.99%**).

**The ceiling was not crossed *by* intraday honesty; it was already crossed by 71pp.** And **T2's
prescribed action does not restore Part A** — capping at k=1 gives 67.67%, still 23× the ceiling,
and there is no smaller integer expression than one contract.

**Independent anchor, no bootstrap.** Walked over the *realized* panel, a `Tradeify_Select_100K`
eval running this construct **busts in March 2020** at every k ∈ {1,2,3} — day 226 / 221 / 217 of
1,878, on **both** clocks, the same day. Realized full-panel max DD is **−$6,527 at k=1**, 2.18× the
$3,000 trail, against +$17,780 net. The MC is not producing an artefact.

### Why intraday honesty moves the single-day figure by nothing — and a correction on the record

For a hard-stopped single-entry construct the excursion is **bounded by the stop**. The first read
in-session was that this makes the worst-day identity structural — that the widest-OR-range day must
have been a stopped one. **That was wrong and is corrected here:** the widest range among *held* days
is **623.5 pt** against **390.5 pt** among stopped days. The identity is empirical:

- Worst stopped day **−$783.82** (2026-06-10, long, range 390.5) — a day that *reached* its floor.
- Deepest held-day excursion **−$681.32** (2025-04-09, long) — **$102.50 shallower**, on a day that
  closed **+$3,433.68**.

So the limb is very far from vacuous *at the day level* — **1,143 of 1,144** held days show an
adverse excursion, mean close-minus-worst gap **$252.81**/contract, max **$4,115.00** — it simply
never approaches the trail on any single day. Trail-binding day is a stopped day on both clocks.

### Controls

`run_seed_paired` is a local re-implementation, so without a reproduction control the delta would
measure the re-implementation rather than the barrier clock. Full control battery (A: intraday-off
reproduction of production `run_seed`; B: day-loop mirror of `orb_lib.orb_backtest`; G: correct-clock
anchor reproduction; non-vacuity; adversarial planted-defect tests) plus the one defect the controls
caught and fixed (a NaN→0.00 excursion clamp on certain early-close days, never affecting the
headline arm) — see [`RESULTS_t2_intraday_bust.md`](../../lab/analysis/orb/orb_mnq_2026-07/RESULTS_t2_intraday_bust.md)
and [`test_t2_intraday_bust.py`](../../lab/analysis/orb_mnq_2026-07/test_t2_intraday_bust.py) (7
passed), the canonical owners.

### Two riders on the level

- **Still a lower bound, for a *different* reason.** `simulate_path` deliberately keeps `peak`
  end-of-day denominated — only the equity *tested* against the floor gains the intraday minimum. If
  Tradeify's trail ratchets off an **intraday** high-water mark, this arm is still optimistic.
  Documented in the function; widening it is its own re-MC. `p99 DD` likewise stays EOD-denominated
  in **both** arms and must not be read as intraday-honest.
- **Geometry: corrected eval, not as-published.** `FIRM_RULES` ships `dd_lock_offset_usd: 100`,
  known-wrong for an evaluation account. Headline makes the lock unreachable per the 2026-07-22
  correction. The as-published lock is **+8.06pp more forgiving** at k=2 (68.95%), so running the
  shipped constant would have understated the bust *on top of* the EOD understatement.

  Both venue facts this measurement rests on are recorded in [Rule 13](../operational_rules.md) form
  (verbatim quote, source, date read, scope) in
  [`RESULTS_t2_intraday_bust.md`](../../lab/analysis/orb/orb_mnq_2026-07/RESULTS_t2_intraday_bust.md),
  the canonical owner: eval accounts carry no drawdown *lock* (help.tradeify.co art. 10495897,
  read 2026-07-22, scoped EVALUATION-ONLY by the source itself), and the real-time breach
  *enforcement* clause carries no phase qualifier, read BROAD per Rule 13's scope rule (same
  source, read 2026-07-30).
- **Sensitivity:** the entry-bar convention (`exclude`, 2,000 sims/seed) gives k=2 **76.62%** —
  ~0.4pp against a 74pp margin. Every verdict identical.
- **Sizing basis:** T2 names `k`, a contract count, while `SIZING-BASIS-BOTH-2026-07-31` records the
  3.0% ceiling as calibrated on the 1R-normalized panel. That objection bit the c1 book because
  cap-binding made the 0.50× haircut nearly inert; it does **not** bite here — standalone single
  instrument, per-trade stop *is* the OR range, k ∈ {1,2,3} far under both the 11-contract MNQ
  allocation and the 80-contract account cap, nothing cap-bound. Q-COMPOSE-1's ORB column at 0.37% of
  $200K ≈ $740/R against ≈$154/R here is **not comparable** to these, and predates the lock fix.

### Disposition — owed, and deliberately not taken here

**No trigger is declared fired or unfired, and no k policy moves.** T2's two readings disagree;
choosing between them is a ruling, and §5 forbids loosening a §4 trigger without a superseding ADR —
**reading it in whichever direction the data now favours is the same error class**, which is exactly
what the 2026-07-31c entry declined to do with RF < 1. The revert action, if T2 is ruled fired, is a
superseding ADR; this addendum is the measurement it would rest on.

**A second thing for the same ruling, surfaced by the measurement.** §4's H limb (b) reads
*"survivable, i.e. retains positive single-day headroom against the $3,000 trail under
intraday-honest bust accounting."* That is now measured and **satisfied** — $1,432 at k=2. Part A
bust is 77.01% and the realized account dies in March 2020. **H could be argued RESOLVED on limb
(b)'s own wording while the leg is unfundable**, because limb (b) measures single-day headroom and
not account survival. Flagged for the same operator pass; tightening a falsifier after seeing the
data is not available to this addendum either.

**Not carried into the operator queue** — per §6's own rule (*"carry into the operator queue only if
it earns operator hours"*), it blocks nothing on the B7 / M1 critical path and queues behind the
standing board.

### What is now closed vs still owed

- **Closed:** the `intraday_low=` limb itself (fed, controlled, reproducible); T2 **measured**.
- **Owed:** the **T2 disposition** + the limb-(b) reading (one operator pass) · the fade program's
  open rulings · T3 at **2026-11-08**. H remains **open**.

> **↑ Status appended 2026-08-03 — the two owed items above are DISCHARGED.** The operator ruled
> **T2 FIRED** on the Part A bust reading, escalated past T2's own (inert) cap-at-k=1 remedy, and
> ruled that **limb (b) keeps its literal wording** (stays SATISFIED at $1,432). **H is no longer
> open:** ORB-MNQ-1 is re-`PARKED` and the payable-Tradeify-leg target is **FALSIFIED** —
> [`2026-08-03-orb-mnq-repark-payability-falsified.md`](2026-08-03-orb-mnq-repark-payability-falsified.md).
> **T3 is moot** (the target is already falsified). Still genuinely owed and untouched: the **fade
> program's open rulings**. The prose above is left as written — it was accurate on 2026-08-02 and
> is retained as dated record, not rewritten.
- **Downstream synced 2026-08-02 (operator-directed):** three stale T2-related clauses corrected,
  marked `VERIFIED 2026-08-02` — see
  [`2026-07-17-0808-packet-delta-and-sequence.md`](../briefs/programs/2026-07-17-0808-packet-delta-and-sequence.md),
  the canonical owner of those clauses and its own correction record.

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-31 | Initial authoring; operator GO in chat; Phase-0 falsifier run before authoring | Joshua (GO) + Cursor |
| 2026-07-31 | Addendum 2026-07-31b — sibling harvest-lane Stage-0 kill; acceptance ungated from sibling pre-reg | Cursor (intake research) |
| 2026-07-31 | Addendum rulings 1+2 recorded (open manifests do not bank K; sibling routed to the K=0 fade program); Phase 2 complete; Status → `Accepted` | Joshua (rulings) + Cursor |
| 2026-07-31 | Addendum 2026-07-31c — 16:00 re-export scored; **§4 T1 discharged PASS**; Phase 3 ✅ DONE; RF<1 / negative-2026 recorded as adverse input to 08-08, not as a trigger | Joshua (re-export) + Cursor (measurement) |
| 2026-08-02 | Addendum 2026-08-02 — `intraday_low=` limb fed for the first time; **§4 T2 MEASURED**, disposition **owed** (its two readings disagree; the intraday correction decides neither); limb-(b)-vs-Part-A gap surfaced for the same ruling. No trigger declared, no k policy moved | Claude Code (measurement) |
| 2026-08-03 | **Superseded in part.** Operator ruled the owed T2 disposition: T2 **FIRED** on the Part A bust reading, disposition escalated past T2's own (inert) cap-at-k=1 remedy, and H limb (b) keeps its literal wording. §2 + §4 are no longer in force; ORB-MNQ-1 re-`PARKED`, payability target **FALSIFIED** — [`2026-08-03-orb-mnq-repark-payability-falsified.md`](2026-08-03-orb-mnq-repark-payability-falsified.md). **Header + this row only; no decision text edited** | Joshua (rulings) + Claude Code (recorder) |
| 2026-08-29 | Reader-intercept banner + Addendum 2026-08-29: Addendum 2026-07-31b's K_eff/floor-0.98/AT-the-Cap math for a new MNQ seed is superseded by the 2026-08-04 K-bank disclosure-not-gate ADR (adr-decay-audit discharge) | Claude Code |

## Addendum 2026-08-29 — Addendum 2026-07-31b's K-bank math is superseded (adr-decay-audit discharge)

**Does not amend** §2, §3, §4's trigger table, or any existing addendum's text (Rule 14 — frozen
bodies stay byte-unedited; corrections land as a reader-intercept banner at the top of this file
plus this dated addendum). This addendum is the discharge for a `DECAYED_UNDOCUMENTED` finding: the
frozen Addendum 2026-07-31b asserts, as then-current doctrine, *"MNQ family K bank remains 2 → new
MNQ seed at `K_intrinsic=1` is therefore `K_eff = 3`, DSR floor 0.98 — open, but AT the Cap"* — math
that a later ADR has since changed the inputs to.

**What changed and when.** [`2026-08-04-family-k-bank-disclosure-not-gate.md`](2026-08-04-family-k-bank-disclosure-not-gate.md)
(`Accepted` 2026-08-04, four days after this ADR's Addendum 2026-07-31b) redefined `K_eff` from
`K_intrinsic + K_banked(family)` to **`K_eff = K_intrinsic` only** — `K_banked(family)` is retained
and still computed, but demoted from a gating term to a mandatory *disclosure*, and can no longer
fail a seed. Confirmed live in current doctrine:
[`docs/methodology/strategy_harvest.md`](../methodology/strategy_harvest.md) §1 Requirement 3 —
*"Family K-bank — MANDATORY DISCLOSURE, not a gate"* — and its Clause-K description, *"under the
amended rule a `K_intrinsic=1` seed screens at floor **0.65** on *every* family."* Under that rule, a
new `K_intrinsic=1` MNQ seed today screens at floor **0.65**, not the 0.98/"AT the Cap" figure this
ADR's Addendum 2026-07-31b names — a materially easier bar, not a harder one.

**Why the tooling missed it.** The 2026-08-04 ADR's own §7 Phase-3 repair sweep runs
`rg --no-ignore "K_intrinsic \+ K_banked|K_eff = K_intrinsic \+"` across `docs/` and `lab/` to find
and reader-intercept every restatement of the old formula. That regex is a literal-string match; it
does not fire on this file, because Addendum 2026-07-31b never spells out the formula symbolically —
it states the same rule in paraphrased prose ("MNQ family K bank remains 2 → ... `K_eff = 3`, DSR
floor 0.98"). Verified this session:

```bash
rg -n "K_intrinsic \+ K_banked|K_eff = K_intrinsic \+" docs/adr/2026-07-31-orb-mnq-unpark-payability-target.md
# 0 hits — confirms the repair-sweep regex does not, and did not, catch this file
```

This is a **tooling note, not a defect to fix in the 2026-08-04 ADR itself** (that ADR's own body is
equally frozen under the same Rule-14 convention) — flagged here so a future repair-sweep pass knows
to broaden the pattern to catch paraphrased restatements of the same arithmetic, not just the
symbolic form.

**The raw MNQ bank count is separately, doubly stale.** Even setting the K_eff formula question
aside, the "2" bank figure Addendum 2026-07-31b names (D5 closed 1 + ST-EH-1's MNQ half 1) is itself
outdated as a current count. Per the 2026-08-04 ADR's own **2026-08-18 amendment-log entry** (Notice-phase
closed manifests + a Cap-seat K-bank spend both ruled to bank against the family tally), the current
MNQ figure is **21** (6 + 14 + 1 — see that ADR's amendment log for the full breakdown). Under the
current disclosure-only rule this no longer gates anything, but a reader relying on Addendum
2026-07-31b's "2" as a current count — for any purpose, including simple situational awareness — is
reading a doubly-superseded number: superseded once by the formula change (2026-08-04), and again by
the bank's own growth since (2026-08-18).

**What is unaffected.** This addendum touches only the K-bank arithmetic quoted in Addendum
2026-07-31b's Ruling 1. It does not reopen, reword, or re-rule §2's unpark decision, §4's trigger
table (already correctly superseded-in-part by
[`2026-08-03-orb-mnq-repark-payability-falsified.md`](2026-08-03-orb-mnq-repark-payability-falsified.md)
for T1/T2/T3/T4, per this file's own header field), Addendum 2026-07-31b's Ruling 2 (sibling
residual routing), or Addendum 2026-07-31c / 2026-08-02's T1/T2 measurements — none of which turned
on the K-bank figure. Those addenda "stand as `Accepted` record," per this file's own header, exactly
as before.
