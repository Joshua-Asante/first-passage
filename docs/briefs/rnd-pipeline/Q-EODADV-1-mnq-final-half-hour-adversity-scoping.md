# Q-EODADV-1 — What makes the final RTH half-hour adverse for a trend-aligned MNQ intraday position?

**Status:** `CLOSED — FALSIFIED 2026-08-01 (da309ce)` — Stage-0 mechanism scoping; **$0 / K=0 / MNQ Cap seat unspent** (true and surviving)
**Authored:** 2026-08-01
**Closed:** 2026-08-01 (`da309ce`) — FALSIFIED
**Authors:** Joshua (direction 2026-08-01: "make a pre-registered question about why the last half hour should be adverse and use that to find hypotheses") + Claude Code (Fable 5)
**Parent question:** Q-SESSCONF-1 (`d88a47e`) — this forks the *mechanism* limb its §5 declared out of scope
**Loop:** Inquire-phase Pre-Q — closure gates on one channel decomposition plus one uncontaminated bar-level test
**Artifact path:** `docs/briefs/rnd-pipeline/Q-EODADV-1-mnq-final-half-hour-adversity-scoping.md`

**Why this exists.** The 15:30 exit is currently barred — not because it is wrong, but because it
was found by search. [`ADR 2026-07-31 §5`](../../adr/2026-07-31-orb-mnq-unpark-payability-target.md)
forbids *"adopting the 15:30 exit because it backtests better."* The **only** route that would
legitimately license an earlier exit is a mechanism established **before** scoring and
**independently of the P&L curve that revealed the effect**. This brief is that route, and it is
designed so it can return "there is no mechanism" cheaply.

---

## §0 — Rule 0 reads (verified 2026-08-01 at `d88a47e`, worktree clean)

| Source | Anchor | What it supplies |
|---|---|---|
| [`docs/adr/2026-07-31-orb-mnq-unpark-payability-target.md`](../../adr/2026-07-31-orb-mnq-unpark-payability-target.md) §3 Finding 1, §5 | `b22aef8` 2026-07-31 | The symptom (16:00 vs 15:30: meanR +0.0626 vs +0.0778; **+2.1pp more stop-outs**, 38.0% vs 35.9%; −$5,832) and the standing bar on adopting 15:30. |
| [`docs/briefs/rnd-pipeline/Q-SESSCONF-1-...md`](Q-SESSCONF-1-mnq-session-confluence-longer-hold-scoping.md) | `d88a47e` 2026-08-01 | The 12-cell ladder, the contaminated curve, and the ceiling-only discipline this brief inherits. |
| [`ops/instruments/MNQ.md`](../../../ops/instruments/MNQ.md) N3, N5, W3 | `66c2a14` 2026-07-31 | N3: both exit-redesign spaces pre-killed order-free (**median 0.34R adverse excursion on winners**; 0.50R median close give-back "real but unharvestable"). N5: D5 intraday momentum **statistically absent** on modern MNQ. W3: the 1m feed cannot fill an execution layer. |
| [`lab/archive/d5_recost_2026-07/RESULTS.md`](../../../lab/archive/d5_recost_2026-07/RESULTS.md) | via MNQ.md N5 / `e2658bf` | **The uncontaminated prior**: `corr(r_rod, r_last)` +0.081 (IS 2010-18) → **+0.024** (OOS 2019-26); gross Sharpe +0.88 → −0.13. Pre-registered, freeze `2dad8f9` precedes results. |
| [`lab/analysis/orb/orb_universe_2026-06-22/orb_lib.py`](../../../lab/analysis/orb/orb_universe_2026-06-22/orb_lib.py) L248–330 | `dcfe83e1…` (sha256, byte-identical across trees) | Engine semantics: stop = opposite OR extreme (a **fixed level set in the first 30 min**), exit at session close, **no profit target**. This is what makes the stop-out channel mechanically available. |

---

## §1 — The symptom, and the contamination that constrains how it may be explained

**Symptom (measured, Q-SESSCONF-1 sweep at `d88a47e`, engine verbatim, Tradeify economics).**
Decomposing the session into the ladder's marginal blocks, per-minute contribution to `meanR`:

| Block (ET) | per-min ×1e5 | | Block (ET) | per-min ×1e5 |
|---|---:|---|---|---:|
| 10:45–11:00 | +61.3 | | 13:15–13:45 | +48.3 |
| 11:00–11:15 | +7.3 | | 13:45–14:15 | −11.0 |
| 11:15–11:45 | +41.7 | | 14:15–14:45 | +20.0 |
| 11:45–12:15 | +38.3 | | 14:45–15:15 | +47.3 |
| 12:15–12:45 | +7.7 | | **15:30–16:00** | **−50.7** |
| 12:45–13:15 | −11.7 | | *prior 10 blocks* | *mean +24.9, sd 26.0* |

**z = −2.90.** A constant-hazard / pure-time-at-risk null predicts z ≈ 0. So the final block is not
"more exposure" — it is anomalous. That is the phenomenon.

**The contamination, stated plainly.** The table above comes from the very exit-time P&L curve that
motivated the question. It is legitimate as a **symptom description** and is *not* admissible as
confirmation of any mechanism — using it both to generate and to confirm is the
`leading-indicator + P&L-gate = rationalized overlay` failure. **Every confirmatory test in §6
therefore runs on data this curve did not reveal:** underlying bar returns and realized ranges, plus
a stop-out/give-back decomposition the curve never exposed.

---

## §2 — Prior art, and the prior that leans *against* the obvious answer

- **The obvious hypothesis is already weakened by our own data.** The intuitive story is "the day's
  move reverses into the close." But D5-RECOST measured `corr(r_rod, r_last)` at **+0.024 OOS** on
  modern MNQ — weakly *positive*, i.e. the final block mildly **continues** the day's move. If that
  holds, a directional-reversal explanation is the wrong one, and it should be *rejected* by §6
  rather than assumed. Recording this before the test so the result cannot be reverse-fitted.
- **MNQ.md N3** already measured a **0.50R median close give-back**, and judged it *"real but
  unharvestable"* — via an order-free counterfactual over stop and target redesigns. N3 did **not**
  test a *time-based* exit, which is why this question is not a duplicate of it.
- **Q-SESSCONF-1** (parent) closed the hold-window *ceiling* question and explicitly deferred the
  mechanism limb. Its §5 forbids adopting an argmax exit; this brief inherits that intact.
- **The raised bar** (`rejected_candidates.md` L416) admits a new candidate on clause 1 — *a
  mechanism outside the mapped cost-ratio-lever set*. An end-of-session microstructure mechanism is
  a candidate for clause 1 in a way "a different exit time" is not. **Whether it qualifies is an
  operator ruling at §8, not an assumption here.**

---

## §3 — Question

**Pre-Q gate test:** the question names the anomaly and the independence requirement; it does not
name an exit time, a filter, or a construct.

**Q-EODADV-1:** The final RTH half-hour contributes a **−2.9σ** per-minute outlier to a trend-aligned
MNQ intraday position — **what mechanism, if any, produces it, and can that mechanism be established
independently of the exit-time P&L curve that revealed it?**

---

## §4 — Falsifiable hypothesis (H-EODADV-1)

Three mutually exclusive mechanism families, discriminated by **which channel carries the loss**.
The 16:00-vs-15:30 `meanR` delta (−0.0152) decomposes exactly into:

- **(i) stop-out channel** — trades that survive to 15:30 but are stopped between 15:30 and 16:00, truncating at −1R.
- **(ii) give-back channel** — trades that survive to 16:00 in both worlds but close worse than they stood at 15:30.

| | Mechanism | Predicts | Independent (uncontaminated) test |
|---|---|---|---|
| **H-A** | **Directional reversal** — the day's move partially reverses into the close | channel (ii) dominates | `corr(r_10:00→15:30, r_15:30→16:00)` on MNQ bars is **significantly negative** |
| **H-B** | **Variance expansion against a fixed stop** — the final block carries elevated realized range with ~zero drift; a far-but-fixed OR stop is simply exposed to more noise | channel (i) dominates | realized range per minute in 15:30–16:00 is **elevated** vs the session mean, while mean return is ~0 |
| **H-C** | **Null — pure time-at-risk** | neither; effect vanishes under proper normalization | already **z = −2.90** against this, to be re-tested on the confirmatory split |

**H-EODADV-1:** *If* the channel decomposition assigns ≥ **60%** of the −0.0152 delta to one channel
**and** that channel's independent bar-level prediction confirms at p < 0.05, *then* the corresponding
mechanism is established and an exit time **derived from that mechanism's own profile** becomes
licensable; *otherwise* no mechanism is established, the 15:30 exit stays barred, and this closes.

**Accept (RESOLVED)** iff one channel ≥ 60% **AND** its independent test confirms.
**Reject (FALSIFIED)** iff no channel reaches 60%, **or** the dominant channel's independent test fails.
**AMBIGUOUS-HOLD** iff the channels split 40–60% (mechanisms co-present and unseparated at this n).

*Sizing note, pre-registered:* +2.1pp of trades flipping to −1R explains the full −0.0152 delta iff
those trades would otherwise have closed near **−0.28R**. That is plausible, so **H-B is
quantitatively sufficient on its own** — stated now so a confirmation of H-B is not later reported
as a surprise.

---

## §5 — Forbidden moves

- **Taking the exit time from the P&L curve once a mechanism confirms.** The whole point of this
  brief is that the exit must be **predicted by the mechanism's own profile** — if the realized-range
  profile says elevation begins at 15:00, the licensed exit is 15:00 **even though 15:30 scores
  better**. Reverting to the argmax after "confirming a mechanism" is the rationalized-overlay
  failure wearing a mechanism as cover, and it would re-inflate K to the full sweep size (K_eff 14,
  floor 1.262 — which the 15:30 cell's +1.076 fails).
- **Using the Q-SESSCONF-1 ladder as confirmation.** It is the symptom. It is burned (§1).
- **Reporting H-A as confirmed on a weak-positive correlation.** The pre-existing D5 reading is
  **+0.024**; a "not significantly positive" result is *not* evidence of reversal.
- **Re-deriving `corr(r_rod, r_last)` on a hand-picked window** until it turns negative — that is
  best-of-window, which D5-RECOST §5 already forbids on this exact statistic.
- **Treating a confirmed mechanism as authorization to change the live construct.** It licenses a
  *pre-registered candidate*, nothing more; the parameter axis stays LOCKED and D5 stands until a
  superseding ADR says otherwise.
- **Folding this into ORB's existing manifest to avoid spending K.** If it produces a candidate, it
  is a new candidate and is counted as one.

---

## §6 — Gate criteria

| Verdict | Trigger | Disposition |
|---|---|---|
| `RESOLVED` | One channel ≥ 60% of the −0.0152 delta **AND** its §4 independent bar-level test confirms at p < 0.05 | Mechanism established. Author a pre-registration for a **mechanism-derived** exit variant — exit time read off the mechanism profile, `K_intrinsic = 1`, `K_eff = 3`. Operator GO required before any manifest. |
| `FALSIFIED` | No channel ≥ 60%, **or** the dominant channel's independent test fails | Close at $0/K=0. The 15:30 exit stays barred and ADR 2026-07-31 §5 stands unamended. Record that the give-back is real and *mechanism-less*, strengthening N3's "unharvestable." |
| `AMBIGUOUS-HOLD` | Channels split 40–60% | Two mechanisms co-present and unseparated at this n. Name the re-test condition; do **not** license an exit change on a split verdict. |

> **SUPERSEDED PREFIX 2026-08-06 (claim-alignment M37):** Phase 1 **did run** and returned `FALSIFIED` — see [`lab/analysis/orb/eodadv_mnq_2026-08/RESULTS.md`](../../../lab/analysis/orb/eodadv_mnq_2026-08/RESULTS.md) (headed FALSIFIED; cites this brief frozen at `43cdde0`). The next sentence is retained as the **freeze attestation** only.

**Frozen before Phase 1.** Phase 1 has not run.

---

## §7 — Execution plan (self-executing; K=0, $0, no pull)

- **Phase 0** — re-verify §0 anchors; pin panel sha256 (`81c05e9a…`) and engine sha256 (`dcfe83e1…`).
- **Phase 1 — channel decomposition.** Instrument the engine's own output (`stopped`, `R`, `entry_tod`)
  at `close_tod` 15:15 and 15:45 on the **same** trade set; partition the −0.0152 delta into (i) and
  (ii). Report both channels' share. No new engine logic — this reads arrays `orb_backtest` already
  returns.
- **Phase 2 — independent bar-level tests** (no ORB P&L anywhere in this phase): (a)
  `corr(r_10:00→15:30, r_15:30→16:00)` with HAC standard errors; (b) realized range per minute by
  time-of-day across the session, with the 15:30–16:00 block tested against the session distribution.
- **Phase 3 — verdict** against §6; land `lab/analysis/orb/eodadv_mnq_2026-08/RESULTS.md` with both
  channel shares, both independent tests, and the verdict.

---

## §8 — Operator gate (before any candidate arises from this)

Two rulings are owed **only if §6 returns RESOLVED**, and neither is self-takeable:
1. Does an end-of-session microstructure mechanism satisfy raised-bar **clause 1** ("outside the
   mapped cost-ratio-lever set"), or is it still a hold-time re-tune wearing a mechanism?
2. Spending the MNQ family's **last** `K_intrinsic=1` Cap seat.

---

## §9 — Closure record format

`docs/briefs/closures/Q-EODADV-1-closure-{resolved,falsified,ambiguous}.md`, stating: channel shares,
both independent test statistics, what §4 predicted vs what happened, and whether the Cap seat
remains unspent.

---

## §10 — Audit hooks (runnable)

```bash
# 1. Freeze-before-run.
git log --format='%h %ci' -1 -- docs/briefs/rnd-pipeline/Q-EODADV-1-mnq-final-half-hour-adversity-scoping.md
ls lab/analysis/orb/eodadv_mnq_2026-08/ 2>/dev/null || echo "no results yet, as expected pre-run"

# 2. Seat still unspent.
ls discovery_manifests/ | grep -iE "eodadv|sessconf" && echo "VIOLATION" || echo "OK: no manifest, K unspent"

# 3. The uncontaminated prior is quoted correctly (+0.024, not a negative number).
rg -n "0\.024|corr\(r_rod" ops/instruments/MNQ.md

# 4. The standing bar on the 15:30 exit is still in force and unamended.
rg -n "Adopting the 15:30 exit" docs/adr/2026-07-31-orb-mnq-unpark-payability-target.md

# 5. Exposure-control falsifier reproduces (z = -2.90 from the frozen ladder).
rg -n "z = |15:15-15:45" lab/analysis/orb/sessconf_mnq_2026-08/RESULTS.md
```

---

## Verification

```bash
PYTHONIOENCODING=utf-8 python C:/Users/joshu/.claude/skills/brief-authoring/scripts/check_brief.py \
  docs/briefs/rnd-pipeline/Q-EODADV-1-mnq-final-half-hour-adversity-scoping.md --type inquire

git log -1 --format='%h %ci' -- docs/adr/2026-07-31-orb-mnq-unpark-payability-target.md   # b22aef8
git log -1 --format='%h %ci' -- ops/instruments/MNQ.md                                    # 66c2a14
rg -n "38\.0%|35\.9%|\+0\.0778|\+0\.0626" docs/adr/2026-07-31-orb-mnq-unpark-payability-target.md
```
