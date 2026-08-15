**Theme:** c1
**Status:** ACTIVE — how much an added leg cuts dead weeks on the c1 book
# Liveness diversification — how much does an added leg cut dead weeks?

**Date:** 2026-08-02. **Trigger:** operator question — *"what fraction of the 82 dead weeks would a
Wed/Thu-firing leg cover?"* — arising from the observation that S7 session-disjointness (wanted to
avoid `flatten_first` collisions) and cadence (wanted to fill dead weeks) ask for the **same
property**. Read-only compute on the committed 07-23 daily panel; **no K spend, no new data, no
manifest, no gate moved, nothing armed, $0.**

**Scope, stated up front: this is LIVENESS ACCOUNTING, not candidate evaluation.** It measures how
many idle-rule-exposed weeks a leg with a given firing pattern would cover. It says **nothing**
about whether such a leg exists, has edge, clears the cost law, the DSR floor at banked K, the
regime gate, or the 3.0% bust ceiling. A leg that covers every dead week and has no edge is worth
nothing.

## §0 — Anchors (reproduced before anything new was read off)

Panel: [`tradeify_book_composition_2026-07-23/out/daily_panel.csv`](../tradeify_book_composition_2026-07-23/out/daily_panel.csv)
(committed; 1,556 bdays, 2020-08-04 → 2026-07-21). Week bucketing and edge-week censoring copied
verbatim from [`c1_cadence_inactivity_2026-08-02/gap_cadence.py`](../c1_cadence_inactivity_2026-08-02/gap_cadence.py)`:115-124`.
**The harness refuses to report new numbers unless these reproduce** (`liveness.py:107-113`):

| Anchor | Expected | This run |
|---|---|---|
| Weeks in panel | 312 | **312** |
| Zero-trade Mon–Fri weeks | 82 (26.3%) | **82 (26.3%)** |
| Longest dead run | 4 weeks | **4** |
| MYM / MNQ trading days | 191 / 190 | **191 / 190** |
| MYM per-eligible-session entry rate | ~30.7% (RUNBOOK) | **191/623 = 30.7%** |

Re-run is **byte-identical** (fixed seeds: permutation 20260802, MC 20260803).

## §1 — The S7 occupancy pin is confirmed by realized trades, and Wed/Thu are *completely* empty

S7's occupancy is sourced from **locked Pine session filters**, deliberately *not* from observed
frequency. This run checks the realized panel against it — an independent corroboration that did not
exist:

| Leg | Mon | Tue | Wed | Thu | Fri | Pine claim | Off-claim trades |
|---|---|---|---|---|---|---|---|
| MYM (Striker DJ30) | 0 | 96 | **0** | **0** | 95 | Tue, Fri | **NONE** |
| MNQ (Striker NAS100) | 85 | 105 | **0** | **0** | 0 | Mon, Tue | **NONE** |

**Zero off-claim trades in six years.** The pin holds exactly.

**The structural fact this exposes: Wednesday and Thursday are 622 of 1,556 business days — ~40% of
the panel — and the book has never traded a single one of them.** Dead weeks are not an accident of
timing; two full weekdays are unreachable by construction.

## §2 — Realized liveness diversification (measured, no independence assumption)

The two legs are each other's natural experiment, so the headline number needs no modeling:

| Book | Dead Mon–Fri weeks | Longest dead run |
|---|---|---|
| MYM alone | 150 / 312 (48.1%) | **9 weeks** |
| MNQ alone | 151 / 312 (48.4%) | **10 weeks** |
| **Both (the c1 book)** | **82 / 312 (26.3%)** | **4 weeks** |

Adding the second leg cut dead weeks by **≈45%** (150→82 for MYM, 151→82 for MNQ) and **more than
halved the worst dead run** (9–10 weeks → 4).

**This is a large, realized effect, and it is not a P&L effect.** On the 52 days both legs trade,
corr(daily P&L) = **−0.13** — essentially nil. The legs do not diversify *returns*; they diversify
*liveness*. That property has never been named or scored anywhere in the screening apparatus.

## §3 — Common-mode test: do the legs go quiet in the *same* weeks?

The obvious objection to §2 generalizing is that dead weeks may be dead for a common reason (chop,
low vol), in which case a third leg would also be quiet in exactly those weeks. **Tested, not
assumed:**

| Quantity | Value |
|---|---|
| P(MNQ week dead) | 0.484 |
| P(MNQ week dead \| MYM week dead) | 0.547 |
| **Common-mode lift** | **1.13×** |
| Joint-dead weeks: observed vs independence | 82 vs 72.6 |
| Permutation p(≥ observed), n=20,000 | **0.022** |

**Quiet weeks do coincide more than chance — but only mildly.** The effect is statistically
detectable (p = 0.022) and practically small (13%). So the common-mode objection is **real and
bounded**: an independence-based estimate is an upper bound, but it is only ~13% optimistic, not
2×. This is the finding that lets the §4 curve be taken seriously.

## §4 — Coverage: what a Wed/Thu leg would actually buy

**Every one of the 82 dead weeks is a full 5-business-day week containing exactly 2 Wed/Thu
sessions** — none is holiday-shortened (mean bdays 5.00, min 5). So the **ceiling is 100%**: a leg
firing every Wed and Thu drives dead weeks to **zero**.

Realistically, at per-session entry rate `p` (both columns shown — the discounted one applies the
measured 1.13× common-mode lift):

| p | Dead weeks left (indep.) | Covered | Dead weeks left (lift-adj.) | Covered |
|---|---|---|---|---|
| 0.10 | 66.4 | 19.0% | 75.0 | 8.5% |
| 0.20 | 52.5 | 36.0% | 59.3 | 27.7% |
| **0.307** *(incumbent rate)* | **39.4** | **52.0%** | **44.5** | **45.8%** |
| 0.40 | 29.5 | 64.0% | 33.3 | 59.3% |
| 0.50 | 20.5 | 75.0% | 23.2 | 71.8% |
| 0.75 | 5.1 | 93.8% | 5.8 | 92.9% |
| 1.00 | 0.0 | 100% | 0.0 | 100% |

**Headline: a third leg firing Wed/Thu at the incumbents' own entry rate (~30.7%) would cover
roughly half the dead weeks — 82 → ~40–45, i.e. the book's dead-week rate 26.3% → ~13–14%.**

## §5 — But it does NOT remove the tail, and that is the decision-relevant part

The idle rule's exposure unit is the **consecutive** dead run, not the count. Seeded MC (n=20,000,
lift-adjusted):

| p | Mean longest run | p95 | Max |
|---|---|---|---|
| baseline (no third leg) | 4 | 4 | 4 |
| 0.10 | 3.91 | 4.0 | 4 |
| 0.20 | 3.45 | 4.0 | 4 |
| **0.307** | **2.91** | **4.0** | **4** |
| 0.50 | 2.04 | 3.0 | 4 |
| 1.00 | 0.00 | 0.0 | 0 |

**At any realistic entry rate the p95 longest run stays 4 weeks.** A Striker-like third leg reduces
how *often* the book is exposed; it does not remove the *worst case*. Only near-daily firing
(p → 1) eliminates it.

**Consequence: liveness diversification is not a substitute for the token mechanism.** It lowers the
frequency of the obligation; the tail — the 4-consecutive-dead-week stretch, against an enforcement
consequence that is irreversible account deletion — survives. Both are wanted, and the token remains
the thing that closes the tail.

## §6 — Findings

1. **The S7 pin is realized-confirmed** (zero off-claim trades in six years), and **~40% of all
   business days are structurally unreachable** by the current book.
2. **Liveness diversification is real, large, and measured** — the second leg cut dead weeks ~45%
   and halved the worst run, on a leg pair whose P&L correlation is −0.13. **Legs can diversify
   liveness without diversifying returns.** No screen scores this.
3. **The common-mode objection is bounded at 1.13×** (p = 0.022) — detectable, small, and not
   large enough to defeat the mechanism.
4. **A Wed/Thu leg at incumbent entry rate halves dead weeks** (82 → ~40–45).
5. **It does not remove the 4-week tail at any realistic entry rate** — so it complements, and does
   not replace, the token mechanism.
6. **S7 and cadence want the same property**, so session-disjointness is not merely a constraint to
   satisfy — it carries a measurable liveness upside. That argues for adding a **liveness limb** to
   the third-leg screen, scored from locked Pine session filters (never from observed frequency,
   per S7's own rule).

## §7 — What this does NOT license

- **No candidate is admitted, proposed, or searched for.** This is liveness accounting; edge, cost
  law, DSR floor at banked K, regime gate and the 3.0% bust ceiling are all untouched and all still
  bind. **A Wed/Thu constraint NARROWS the search space** — it may well be empty, and that is not
  evidence against the constraint.
- **No screen is amended.** Finding 6 is a recommendation to the third-leg spec's owner, not an edit.
- **No pin, gate, allocation, `dd_protection` constant, lifecycle rung, or Pine touched. Nothing
  armed.** Q-COMPOSE-1 stands: composing raises bust, and a liveness argument does not answer it.
- **These are panel-geometry cadence statistics**, sizing-invariant at the zero/non-zero level (so
  the dead-week counts transfer), but they are **not** a claim about P&L, bust, or pass rate.

## Reproduction

```bash
python lab/analysis/c1_liveness_diversification_2026-08-02/liveness.py
```

Reads only the committed `daily_panel.csv`; fixed seeds (20260802 / 20260803); re-run verified
byte-identical; outputs under `out/` are committed.
