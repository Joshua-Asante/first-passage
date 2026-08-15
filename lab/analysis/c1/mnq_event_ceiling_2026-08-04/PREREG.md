# `MNQBASE-1` Step 1 — VERDICT PRE-REGISTRATION: the independent-event ceiling on MNQ

**FROZEN ON THIS FILE'S INTRODUCING COMMIT. No criterion below may move after the first real count
exists. Zero event counts have been computed at freeze time.**

**Parent:** [`MNQBASE-1` scoping](../../../../docs/briefs/rnd-pipeline/MNQBASE-1-tradeify-shaped-base-construct-harvest-scoping.md) §7 Step 1.
**Purpose:** bound the entire base-construct search **before any candidate is sourced**. If even a
maximally generous ceiling is below 3 independent events/day, **L1 fires** and no mechanism can
rescue a single-instrument construct — the answer is a multi-leg book.
**K:** `0` — one-way bounding measurement, no GO state (§5). **Cost:** `$0.00` (MNQ 1m on disk).
**No manifest. No Cap seat.** **Class:** order-free, mechanism-free, strategy-free.
**Authored:** 2026-08-04 · Claude Code (Opus 5), operator-directed.

---

## §0 — Rule 0 reads (verified this session 2026-08-04)

- **[`core/firm_rules.py`](../../../../core/firm_rules.py) `Tradeify_Select_100K` @ `2345095`** — the live target: `max_dd_pct 3.0` ($3,000 rope), `profit_target_pct 6.0` ($6,000), **`cost_per_side_usd 0.91`**, `micro_contract_cap 80`, `inactivity_max_idle_days 5`. MNQ point value **$2.00/pt**, tick 0.25 pt ([`MNQ.md`](../../../../ops/instruments/MNQ.md) header).
- **[`lab/analysis/c1/eval_inverse_requirements_2026-08-03/RESULTS.md`](../eval_inverse_requirements_2026-08-03/RESULTS.md) @ `1dcde85`** — the spec this bounds: `μ_max = k × r_max × E`, **linear in frequency, capped in size**; **3–8 trades/day** needed; max risk **$275/trade**; **§2 independence is load-bearing** — *"Perfectly correlated k trades at risk r are arithmetically identical to one trade at risk k·r, which collapses to the k=1 row"*. §2a: below **~0.40R** the sign inverts.
- **[`MNQBASE-1` scoping](../../../../docs/briefs/rnd-pipeline/MNQBASE-1-tradeify-shaped-base-construct-harvest-scoping.md) §2.1 T1–T7 @ `077fb7d`** — the target spec whose T2 (3–8 independent trades/day) this measurement bounds, and T5 (flat by 16:00 ET) which fixes the session window below.
- **[`lab/archive/ict_cascade_2026-06-18/PREREG-1M.md`](../../../archive/ict_cascade_2026-06-18/PREREG-1M.md) L52 @ `47cc3eb`** — the tradeability floor precedent: *drop trades with `stop_dist < max(1pt, cost)`*. With `rt_pt` 1.41 this sets the smallest admissible stop and therefore the most generous grid cell in §2.
- **[`lab/analysis/_inbox/ict_mnq_2026-08/build_w_export.py`](../../_inbox/ict_mnq_2026-08/build_w_export.py) `in_roll_window` L88 @ `9aaa578`** — the ±4-day 3rd-Friday roll exclusion, reused unmodified.
- **[`lab/analysis/_inbox/ict_mnq_2026-08/RESULTS_EXP.md`](../../_inbox/ict_mnq_2026-08/RESULTS_EXP.md) @ `d627a53`** — the ceiling-limb pattern this inherits: a perfect-foresight upper bound that **no construct can beat**, whose value is that a FAIL is conclusive while a PASS licenses nothing. Its pre-registered "expected to clear, and uninformative if it does" disclosure is the model for §4's expectation note.
- **`ops/instruments/MNQ.md` W1 @ `55adcaa`** — `.v.0` volume-lead continuous is the TV-`1!` analogue; a wrong continuous choice changes bar **existence**, not just levels. Data below is `MNQ.v.0`, matching every prior study in this campaign.

---

## §1 — What is being measured, and why it is a ceiling

**The quantity.** Partition each session into the **maximum number of disjoint time windows, each
containing a price range of at least `G` points.** That count is the ceiling on independent
`G`-capturing trades available that day.

**Why it is a strict upper bound.** Any trade capturing `G` points must hold across a window whose
high-minus-low is at least `G`. Independent (non-overlapping, T3) trades occupy **disjoint** windows.
Therefore no strategy — at any entry rule, any direction, with perfect foresight — can produce more
than this many independent `G`-capturing trades in that session. It is generous three times over:
it grants perfect direction, perfect timing, and counts a *range* rather than a realized directional
capture from a specific entry.

**What it deliberately is not.** Not a strategy, not an edge estimate, not a fill model. A window
with `G` points of range does not mean a tradeable `G`-point capture with a stop that holds. **The
number is an upper bound and only an upper bound** — its job is to answer whether the frequency T2
requires is *structurally available on this instrument at all*.

---

## §2 — Frozen construction

**Data.** `MNQ.v.0` continuous 1m, databento GLBX.MDP3, on disk at `$0.00`.

**Session window (the verdict window).** **18:00 ET (prior calendar day) → 16:00 ET** — the widest
window consistent with T5's flat-by-16:00 rule, chosen for generosity so that a FAIL is conclusive.
Sessions are keyed by their **16:00 ET close date** (ET, not UTC — MNQ ledger W2). A session is
scored only if it carries ≥ 60 one-minute bars.

**Roll exclusion.** `in_roll_window` (±4 days of the 3rd Friday of Mar/Jun/Sep/Dec) applied at the
session level, inherited. Removes sessions only; it cannot inflate a count.

**The `G` grid — the domain of an existential question, NOT a search.** `G` is fixed by the spec,
not chosen: a trade with stop `s` clearing T1 (edge ≥ 0.40R) net of the 1.41 pt round trip must
gross

    G(s) = 0.40 · s + 1.41   points

| stop `s` (pt) | 2 | 5 | 10 | 20 | 40 |
|---|---|---|---|---|---|
| **`G` (pt)** | **2.21** | **3.41** | **5.41** | **9.41** | **17.41** |
| qty at $275 risk (`137.5/s`) | 68 | 27 | 13 | 6 | 3 |

All five sit inside the 80-micro eval cap, so the risk cap binds **sizing**, never the event count.
`s = 2` is the most generous cell admissible under the `stop_dist ≥ max(1pt, cost)` floor (1.41 pt).

**Counting rule (greedy, deterministic).** From the session's first bar, advance to the earliest bar
`j` at which the running window's `max(high) − min(low) ≥ G`; count one event; restart the window at
`j+1`. Repeat to session end. Greedy-earliest maximises the count, which is the generous direction.

**Verdict statistic.** The **median across scored sessions** of the per-session count, at each `G`.
Median rather than mean: robust to the handful of extreme-range days that would otherwise carry it.

---

## §3 — Question

**Every MNQ construct measured to date misses the eval on frequency, never on per-trade edge — and
nobody has measured whether the frequency is there to be captured.** Realized strategy frequency
(0.35 trades/calendar-day for the incumbent book) is a fact about the strategies built, not about
the instrument. **Is the frequency T2 demands structurally available on MNQ at all, at any stop
level that clears the edge threshold?**

Symptom-only: *we do not know whether we have been failing to find the opportunities, or whether
they are not there.* Names no mechanism and proposes no construct.

---

## §4 — Falsifiable hypothesis

**H-CEIL-1.** MNQ offers at least **3 independent `G`-capturing windows per session** at **some**
`G` on the §2 grid — i.e. the frequency T2 requires is structurally available.

**Falsifier — frozen trigger table.**

| # | Trigger | Threshold | Verdict |
|---|---|---|---|
| C1 | scored sessions | **< 250** | **`INSUFFICIENT-N`** — a bounding claim needs ≥ ~1 year of sessions |
| C2 | **max over the `G` grid** of the median per-session count | **< 3** | **`FALSIFIED` → parent L1 fires.** Single-instrument MNQ cannot reach T2 at any admissible stop. Routes to multi-leg book composition |
| C3 | max over the grid ≥ 3 but **< 3 at every `G` ≥ 5.41** (i.e. only the tightest, least holdable stops reach it) | — | **`AMBIGUOUS`** — available in principle, but only where T4 (stops that hold) is least credible |
| C4 | median ≥ 3 at some `G` ≥ 5.41 | — | **`RESOLVED`** — frequency is structurally available; **the constraint is mechanism-side, not instrumental.** Licenses nothing (§5) |

**Pre-registered expectation — and a correction to the parent brief's, recorded before running.**
`MNQBASE-1` §4 called **L1 firing "the single most likely outcome"** on the strength of the
incumbent's 0.35 trades/calendar-day. **That reasoning conflates two different quantities.** Realized
strategy frequency is a property of the constructs built; the event ceiling is a property of the
instrument. MNQ's daily range routinely runs into the hundreds of points, so **a ceiling well above
3/day at tight `G` is the more likely outcome**, and it would *not* contradict the incumbent's 0.35 —
a high ceiling with low realized frequency is exactly what "we have not built anything that fires
often" looks like. **A high ceiling is therefore expected and is NOT a positive result** — it
relocates the problem from structural to mechanism-side and licenses no candidate. Recorded here so
that outcome cannot be retrofitted as a discovery.

---

## §5 — Forbidden moves

- **FM-1 — Reading a high ceiling as evidence that a construct exists.** It is an upper bound built on perfect foresight; the gap between it and any realizable strategy is the entire problem. `RESOLVED` here licenses **nothing** and opens **no** candidate.
- **FM-2 — Selecting the "best" `G` and reporting it as the answer.** The grid is the domain of one existential question (§4). The verdict is `max over grid`, declared before running; quoting a single cell as *the* ceiling is selection.
- **FM-3 — Re-deriving `G(s) = 0.40s + 1.41` with a different edge or cost** after seeing the counts. The 0.40R threshold is the §2a inversion point and the 1.41 pt round trip is the Tradeify basis; both are inputs, not knobs.
- **FM-4 — Widening the session window, dropping the roll exclusion, or switching to mean-across-sessions** to lift a count that came in low. Each is an outcome-conditional loosening; the window is already the most generous T5 permits.
- **FM-5 — Treating a range-window as a tradeable opportunity** in any downstream citation. §1 states the bound explicitly and every quotation of these numbers must carry it.
- **FM-6 — Any `core/`, lock, allocation, `dd_protection`, lifecycle, Pine, rail, or `LEG_MAP` change.**

---

## §6 — Gate criteria and typed dispositions

| Verdict | Trigger | **Disposition (pre-registered)** |
|---|---|---|
| `INSUFFICIENT-N` | C1 | **STOP** — cannot bound on this panel; re-proposal bar is more sessions, which exist, so this branch should not fire |
| `FALSIFIED` | C2 | **ITERATE → Identify.** Parent L1 fires. Entry packet: the per-`G` curve, the session distribution, and T1–T7. Successor question is **book composition across instruments**, not a better MNQ construct |
| `AMBIGUOUS` | C3 | **ITERATE → Investigate.** Frequency exists only at stops T4 makes least credible; packet carries the curve and the stop-holdability tension |
| `RESOLVED` | C4 | **ITERATE → the parent's Step 2.** Frequency is available; the intake pass proceeds against §2.3's pre-filters. **Names no candidate** |

**Board write** owed at closure in all branches.

---

## §10 — Audit hooks (runnable)

```bash
# Freeze ordering must be git-auditable: this file's commit precedes RESULTS.md's.
git log --format='%h %cs' -- lab/analysis/c1/mnq_event_ceiling_2026-08-04/PREREG.md | tail -1
git log --format='%h %cs' -- lab/analysis/c1/mnq_event_ceiling_2026-08-04/RESULTS.md | tail -1

# The cost basis and point value the G grid is built on (expect 0.91, and $2.00/pt in the ledger):
python -c "import sys;sys.path.insert(0,'.');from core import firm_rules as F;print(F.FIRM_RULES['Tradeify_Select_100K']['cost_per_side_usd'])"
grep -c '\$2.00/pt' ops/instruments/MNQ.md

# The 0.40R inversion threshold G(s) is derived from:
grep -c "0.40R" lab/analysis/c1/eval_inverse_requirements_2026-08-03/RESULTS.md

# No manifest, no K bound by this measurement (expect 0):
ls discovery_manifests/ | grep -icE "ceil|mnqbase"

# The roll helper is reused unmodified from the frozen adapter:
grep -n "def in_roll_window" lab/analysis/_inbox/ict_mnq_2026-08/build_w_export.py
```

---

## Amendment log (append-only)

- **2026-08-04 — RATIFIED/FROZEN** on this file's introducing commit. No event count existed at
  freeze. §4 records a **correction to the parent brief's stated expectation**, made before running,
  so that the likely high-ceiling outcome cannot later be read as either a surprise or a discovery.
