# ORB-MNQ-1 §4 T2 — intraday-honest bust accounting at the deployed k

**Date:** 2026-08-02 · **Harness:** [`run_t2_intraday_bust.py`](run_t2_intraday_bust.py) ·
**Controls:** [`test_t2_intraday_bust.py`](test_t2_intraday_bust.py) (7 passed) ·
**Reports:** [`t2_intraday_bust_report.json`](t2_intraday_bust_report.json) (headline),
[`t2_intraday_bust_report_excl.json`](t2_intraday_bust_report_excl.json) (sensitivity)

**Trigger under test** — [ADR 2026-07-31 §4](../../../docs/adr/2026-07-31-orb-mnq-unpark-payability-target.md):

> **T2** | Intraday-honest bust accounting (once the 07-30 follow-on `intraday_low=` limb
> lands) re-scores the deployed k | **Threshold:** k=2 single-day bust exceeds the frozen
> 3.0% ceiling | **Action:** k policy capped at k=1; payability target re-scoped by amending ADR

**Cost:** $0. No databento pull, no cost dry-run, no TV export, no operator data spend, no
K spend, no manifest, nothing armed. Pure computation on the cached MNQ.v.0 15m panel
(`_mnq_15m.pkl`, sha256 `81c05e9a4ee319e8…`, 15,757,437 bytes, cached 2026-07-17).

---

## §0 — Verdict

**T2 fires on the ceiling comparison and does NOT fire on its own literal wording, and the
intraday limb is not what decides either.** Three separable statements:

1. **Literal reading — single-day bust: 0 days, unchanged by intraday honesty.** At every
   k ∈ {1,2,3} the worst intraday excursion is *exactly* the worst end-of-day loss
   (−$783.82 × k), and no single day reaches the $3,000 trail on either clock. k=2 keeps
   **$1,432** of single-day headroom, intraday-honest. On this reading T2's threshold is
   **not met**.
2. **Ceiling reading — Part A bust: 77.01% vs 3.0%, 26× over.** But the end-of-day arm
   already reads **74.00%**. The intraday limb moves it **+3.01pp**. The ceiling was not
   crossed *by* intraday honesty; it was already crossed by a wide margin.
3. **T2's prescribed action does not restore Part A.** Capping at k=1 gives **67.67%** —
   still 23× the ceiling. There is no smaller integer expression: k=1 is one contract.

**Independent anchor:** walked over the *actual* realized panel rather than a bootstrap,
a `Tradeify_Select_100K` eval account running this construct **busts in March 2020** at
every k ∈ {1,2,3} — day 226 / 221 / 217 of 1,878, on **both** clocks, same day. Realized
full-panel max drawdown is **−$6,527 at k=1**, 2.18× the $3,000 trail.

**What this does not decide.** Adjudicating T2 — which reading governs, and whether the
action fires — is an operator call under a superseding/amending ADR (§5, Known Trap #12).
Nothing here edits the ADR, the k policy, `core/`, allocation, `dd_protection`, Pine, the
rail, or `LEG_MAP`.

> **DISPOSITION TAKEN 2026-08-03 — this measurement is no longer awaiting a ruling.** The
> operator ruled **T2 FIRED on the Part A bust reading** (reading 2 above governs; reading 1
> does not), and escalated past T2's own Action column because capping at k=1 is **inert**
> (67.67%, 23× the ceiling). **ORB-MNQ-1 is re-`PARKED` and the payable-`Tradeify_Select_100K`-leg
> target is recorded FALSIFIED.** H limb (b) was ruled to **keep its literal wording** and stays
> SATISFIED at $1,432. Also surfaced at adjudication: the frozen survivor-scoring gate's
> **second** limb, P(pass) ≥ 50%, fails at every k (**32.33% / 22.99% / 19.82%**) — so both limbs
> fail, not only the one T2 named. Nothing below is retracted or amended; the numbers stand as
> measured. Governing artifact:
> [`ADR 2026-08-03`](../../../docs/adr/2026-08-03-orb-mnq-repark-payability-falsified.md).

---

## §1 — The gap that was closed

`core/mc/simulation.py::simulate_path` gained an opt-in `intraday_low=` argument on
2026-07-30, because Tradeify enforces the trailing-drawdown **breach** in real time while
the **limit** updates end-of-day. **Nothing ever fed it.** `run_seed`
builds its bootstrap `path` from daily P&L blocks only, so every published bust figure
tests the barrier against the *close* and is a lower bound.

The two venue facts this rests on, in [Rule 13](../../../docs/operational_rules.md) form:

| Quote (verbatim) | Source | Date read | Scope |
|---|---|---|---|
| *"ENFORCED in real-time … your account fails immediately — even if you might have recovered by end of day"* | help.tradeify.co art. **10495897** | **2026-07-30** (in-browser; `WebFetch` 403s) | **STANDING (BROAD)** — no phase qualifier on this clause while its sibling (locking) is scoped to Sim Funded explicitly ⇒ Rule 13 reads the silence BROAD; binds the eval |
| *"Q: Does drawdown lock on Evaluation accounts? A: No. Drawdown only locks on Sim Funded accounts. Evaluation accounts do not have drawdown locking."* | help.tradeify.co art. **10495897** | **2026-07-22** (via the eval-lock correction) | **EVALUATION-ONLY** — the source scopes it itself; no silence to resolve. This is why §4's headline runs the lock unreachable |

Two pieces were missing and are written here:

- **The derivation** — a per-day minimum equity excursion for the ORB construct.
- **A paired bootstrap** — `run_seed` cannot carry a second per-day series, so the same
  drawn block indices are applied to both the P&L panel and the excursion panel.

15m bars are sufficient and this is not a resolution compromise: an OHLC bar records the
actual traded extreme within it, so max/min over a session's bars is the true intraday
extreme at full price precision. Only the *timestamp* of a threshold crossing is lost, and
no quantity here depends on it.

### Derivation

`simulate_path` wants, per business day, the minimum equity excursion in dollars measured
from that day's **opening** equity (entries ≤ 0, unscaled). ORB holds at most one position
per session, so that excursion is exactly the position's worst mark-to-market:

| Day type | Excursion |
|---|---|
| **Stopped** (702 days) | The engine models the exit **at** the opposite OR extreme, so nothing prints below it: excursion ≡ realized P&L ≡ −(range + rt) |
| **Held to close** (1,144 days) | Worst adverse mark over bars from entry through session close — long `min(low) − entry`, short `entry − max(high)`. Bounded strictly above −range, because `stopped == False` means no bar touched the opposite extreme |

Both pay the engine's own `rt_cost_pt` and are clamped ≤ 0.

Note the derivation is **not** `min(Low)` over the session's bars. That would be wrong for
shorts (the adverse extreme is the high) and would count bars before entry and after exit.
It uses the same data at the same cost.

### Structural consequence, stated before the numbers

For a hard-stopped single-entry construct the intraday correction is **bounded by the
stop**. This is the shape the 2026-07-30 primary-source read called out as bounded, as
against the unbounded pyramided-book case — and ORB is squarely the bounded one.

---

## §2 — Controls

| # | Control | Result |
|---|---|---|
| **A** | The paired bootstrap reproduces production `core.mc.simulation.run_seed` bucket-for-bucket with the intraday limb off (identical RNG call sequence) | **PASS** — outcomes, `days_to_pass`, `max_dds` all identical |
| **B** | The day-loop mirror reproduces `orb_lib.orb_backtest` elementwise on all five emitted arrays (`R` / `range` / `side` / `stopped` / `entry_tod`) | **PASS** — n=1,846 |
| **C** | Excursion invariants: every entry ≤ 0; dominates the day's realized P&L; **equals** it on stopped days; never breaches the structural stop floor −(range + rt) | **PASS** |
| **D** | Intraday bust ≥ EOD bust, and pass ≤ EOD pass, at every k | **PASS** |
| **E** | The intraday limb is not vacuous — a planted deep excursion must bust a path the close alone survives | **PASS** |
| **F** | The invariant checker itself fails on three planted defects (excursion above realized; stopped-day mismatch; through-the-floor) | **PASS** — not a vacuous assert |
| **G** | Published correct-clock anchors reproduce | n **1,846**, meanR **+0.0626**, net **$17,780**, WR **46.37%**, stopped **38.0%**, maxDD **−$6,527** — all exact |

Control A is the load-bearing one. `run_seed_paired` is a local re-implementation; without
A, the intraday-vs-EOD delta would measure the re-implementation rather than the barrier
clock. Control F exists because a dominance assert that never fires certifies nothing.

**A defect the controls caught.** The first sensitivity run aborted on Control C: on
early-close days whose entry is the last bar carrying data, the post-entry window is
present-but-all-NaN, and the ≤ 0 clamp silently converted that `NaN` into a spurious
`0.00` excursion — i.e. the most forgiving possible value. Reachable only under the
`exclude` convention; fixed at source. The headline arm was never affected.

---

## §3 — Derivation output

Per contract, full window 2019-05-06 → 2026-07-15, correct clock (exit 16:00), Tradeify
$0.91/side + 1-tick slip (rt = 1.41 index pt).

| Quantity | `include` (headline) | `exclude` (sensitivity) |
|---|---:|---:|
| Trade days | 1,846 | 1,846 |
| Stopped / held to close | 702 / 1,144 | 702 / 1,144 |
| Held days showing an adverse excursion | **1,143** of 1,144 | 1,138 of 1,144 |
| Mean close-minus-worst gap, held days | **$252.81** | $229.82 |
| Max close-minus-worst gap, held days | **$4,115.00** | $4,115.00 |
| Worst realized day | **−$783.82** | −$783.82 |
| Worst intraday excursion | **−$783.82** | −$783.82 |

The two conventions differ in whether the entry bar's own adverse extreme counts (within a
15m bar, the ordering of the extreme against the breakout touch is unknowable). `include`
is the venue-honest direction and is the headline.

**Why the two worst-day figures coincide — and why it is not structural.** My first read
was that the widest-OR-range day must have been a stopped one. **It was not:** the widest
range among held days is **623.5 pt** against **390.5 pt** among stopped days. The identity
is empirical, not forced:

- Worst stopped day: **−$783.82** (2026-06-10, long, range 390.5) — a day that *reached*
  its floor.
- Deepest held-day excursion: **−$681.32** (2025-04-09, long, range 357.5) — **$102.50
  shallower**, on a day that closed **+$3,433.68**. That single day is the $4,115.00 max
  gap: the intraday limb is very far from vacuous *at the day level*; it just never gets
  near the trail on any one day.

So the trail-binding single day is a stopped day, on both clocks. Intraday honesty changes
the single-day picture by exactly nothing.

### Single-day table

| k | worst day, EOD | worst day, intraday | headroom EOD | headroom intraday | days breaching $3,000 |
|---:|---:|---:|---:|---:|---:|
| 1 | −$784 | −$784 | $2,216 | $2,216 | 0 |
| **2** | **−$1,568** | **−$1,568** | **$1,432** | **$1,432** | **0** |
| 3 | −$2,351 | −$2,351 | $649 | $649 | 0 |

Identical under both entry-bar conventions.

---

## §4 — Part A re-MC

Pre-registered protocol, unedited:
[`2026-07-13-prop-survivor-scoring-prereg.md`](../../../docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md)
— **bust ≤ 3.0% ∧ P(pass) ≥ 50%**, Run-2 (consistency 40%), `Tradeify_Select_100K`,
horizon 1500, seeds 42/123/2026, **10,000 sims/seed**, inactivity disabled,
`dd_protection` off. Headline bust read via `preflight.summarize_outcomes`
(daily+static+**trailing**), never `compute_default_config()['bust_rate']` — the F1 trap.

Blocks: 1,878 business days → **375** Mon-anchored 5-day blocks; 1,846 trade days, non-trade
business days flat (P&L 0.0, excursion 0.0), per the Q-COMPOSE-1 `reindex(bdays).fillna(0.0)`
precedent. Both arms draw identical block indices, so the delta is the barrier clock alone.

**Drawdown geometry: CORRECTED eval, not as-published.** `FIRM_RULES` ships
`dd_lock_offset_usd: 100` for this tier, which is known-wrong for an evaluation account —
Tradeify art. 10495897: *"Evaluation accounts do not have drawdown locking."* The headline
makes the lock unreachable (pure fixed-$ trail), per the 2026-07-22 correction; the
as-published lock is kept as a control row.

| k | arm | headline bust | P(pass) | median days | p99 DD | Part A |
|---:|---|---:|---:|---:|---:|:--|
| 1 | EOD | 65.23% | 34.77% | 228 | 3.43% | FAIL |
| 1 | **intraday** | **67.67%** | 32.33% | 220 | 3.41% | FAIL |
| | *delta* | *+2.44pp* | | | | |
| **2** | EOD | **74.00%** | 26.00% | 70 | 3.94% | FAIL |
| **2** | **intraday** | **77.01%** | **22.99%** | 66 | 3.91% | **FAIL** |
| | *delta* | *+3.01pp* | | | | |
| 2 | intraday @ lock $100 *(control)* | 68.95% | 31.04% | 79 | 7.44% | FAIL |
| 3 | EOD | 76.17% | 23.83% | 38 | 4.47% | FAIL |
| 3 | **intraday** | **80.18%** | 19.82% | 35 | 4.44% | FAIL |
| | *delta* | *+4.01pp* | | | | |

**Sensitivity (`exclude` convention, 2,000 sims/seed):** k=1 67.25% · k=2 **76.62%** ·
k=3 79.55%. Every verdict identical; the entry-bar convention is worth ~0.4pp at k=2
against a 74pp margin.

**Geometry control reads the right way:** the corrected (no-lock) geometry is **+8.06pp**
harsher at k=2 than the as-published lock — i.e. running the shipped `dd_lock_offset_usd:
100` would have understated the bust, on top of the EOD understatement.

### Realized-path anchor (no bootstrap)

The actual historical panel, walked through the same barrier:

| k | realized net | realized max DD | EOD arm | intraday arm |
|---:|---:|---:|---|---|
| 1 | +$17,780 | −$6,527 | `bust_trailing` day 226 — **2020-03-16** | same day |
| 2 | +$35,560 | −$13,054 | `bust_trailing` day 221 — **2020-03-09** | same day |
| 3 | +$53,339 | −$19,581 | `bust_trailing` day 217 — **2020-03-03** | same day |

The construct is net-profitable across the panel and still kills the account inside the
first year, at every admissible k, because a $3,000 trail is roughly *half* its realized
drawdown at one contract. The MC is not producing an artefact.

---

## §5 — Honest limits

- **Still a lower bound, for a different reason.** `simulate_path` deliberately keeps
  `peak` end-of-day denominated: only the equity *tested* against the floor gains the
  intraday minimum. If Tradeify's trail ratchets off an **intraday** high-water mark, this
  arm is still optimistic. That scope choice is documented in the function, not introduced
  here; widening it is its own re-MC.
- **`p99 DD` in the table is EOD-denominated in both arms** (same documented choice). It
  moves only because busts truncate paths earlier. Do not read it as intraday-honest.
- **Sizing basis.** T2 names `k`, a contract count, while `SIZING-BASIS-BOTH-2026-07-31`
  records that the 3.0% ceiling was calibrated on the 1R-normalized panel. That objection
  bit the c1 book because cap-binding made the 0.50× haircut nearly inert. It does not bite
  here: this is a standalone single-instrument leg whose per-trade stop *is* the OR range,
  k ∈ {1,2,3} sits far under both the 11-contract MNQ allocation and the 80-contract account
  cap, so nothing is cap-bound and the contract count is the deployable expression.
  Q-COMPOSE-1's ORB column was sized at 0.37% of $200K ≈ $740/R against ≈$154/R here —
  **that figure is not comparable to these**, and it also predates the eval-lock correction.
- **Engine ≠ Pine** (96.9% per-trade parity) and the panel ends 2026-07-15. Both inherited.
- **One position per session** is what makes the derivation exact. It would not transfer to
  a pyramided construct without re-deriving the excursion from the position ladder.

---

## §6 — Two things worth an operator eye

1. **T2's threshold welds two different units.** *"k=2 single-day bust exceeds the frozen
   3.0% ceiling"* joins a **single-day** quantity (a boolean: does any one day breach the
   trail?) to a **Monte-Carlo rate** ceiling. Measured: single-day = 0 days / $1,432
   headroom; MC rate = 77.01%. The two readings disagree, so which one governs is a ruling,
   not a measurement.
2. **§4's H limb (b) can be satisfied while the leg is unfundable.** Limb (b) reads
   *"survivable, i.e. retains positive single-day headroom against the $3,000 trail under
   intraday-honest bust accounting."* That is now measured and **satisfied** — $1,432 at
   k=2. Part A bust is 77.01%. H could therefore be argued RESOLVED on its own wording
   while the account dies in 77% of paths and in the realized history. Flagged, not
   adjudicated: tightening a falsifier after seeing the data is the same error class as
   loosening one.

---

## §7 — Reproduce

```bash
.venv-research/Scripts/python.exe -m pytest lab/analysis/orb_mnq_2026-07/test_t2_intraday_bust.py -q
```

```bash
.venv-research/Scripts/python.exe lab/analysis/orb_mnq_2026-07/run_t2_intraday_bust.py
```

```bash
.venv-research/Scripts/python.exe lab/analysis/orb_mnq_2026-07/run_t2_intraday_bust.py --entry-bar exclude --n-sims 2000
```

Headline run ≈ 9 min. The cached panel is gitignored and resolves from the primary
checkout; a worktree carries only the `.gitignore`.
