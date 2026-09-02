# D2 — Leveraged/inverse-ETF EOD-rebalance flow: bar-ruling (admit-or-reject)

**Type:** free-data-bar ruling (zero-run). **Authored:** 2026-07-24.
**Source:** advisor Avenue D2 (Stage 2) — "leveraged-ETF EOD flow, triggered only on high-intraday-move
days; edge must concentrate on large-move days AND clear 4× cost in the 3:45–4:00 PM window."
**Verdict (this brief):** **FALSIFIED — reject-at-bar** (see §6). Not admitted for a full Pre-Q.

---

## §0 — Rule-0 reads

Read before ruling (concrete repo paths):

- [`docs/rejected_candidates.md`](../../rejected_candidates.md) § "Domain-level tail-exhaustion raised
  bars" **and** the free-data 5th-leg domain roll-up — the re-proposal bar this candidate is judged
  against (three clearance routes: paid/exogenous data the free searches could not access; a new
  venue class relaxing a *binding* wall; or a dated live incident).
- [`docs/rejected_candidates.md`](../../rejected_candidates.md) § "index-dispersion-correlation-premium
  on SPX500" — the entry-format template used in §6 (heading block + `concept-intake-entry` comment
  + bullet).
- [`core/firm_rules.py`](../../../core/firm_rules.py) `Tradeify_Select_100K` — venue constraint:
  `weekend_holds`/overnight = false, EOD flat; the tradable expression is intraday ES/NQ futures.
- [`docs/briefs/programs/2026-07-14-a4-flow-data-fork-scoping.md`](2026-07-14-a4-flow-data-fork-scoping.md) —
  the adjacent flow-data ruling (net-imbalance-only / never-procure) establishing that EOD-flow
  effects in this program are "real as mechanisms but thin / redundant / decaying as tradable alpha."

## §1 — Context and standing doctrine

The advisor ranks D2 as the one *new directional mechanism* worth Stage-2 effort: trade the mechanical
end-of-day rebalance of constant-leverage ETFs on high-intraday-move days, futures-flat by the close
(Tradeify-compatible). Mechanism (real, long-documented — Cheng & Madhavan 2009 and successors): a
leverage-`L` ETF must trade **in the direction of the day's move** near the close to restore constant
leverage; the rebalance size scales ≈ `AUM · L(L−1) · r` in the day's return `r`, so the flow
concentrates on large-`|r|` days and is momentum-amplifying. Tradable expression = ES/NQ futures
(the ETFs track SPX/NDX), which fits the futures-prop venue.

Standing doctrine this ruling sits under: the **free-data 5th-leg / expansion domain is at
tail-exhaustion** (`rejected_candidates.md`, ≈17–22 consecutive terminal closures with 0 admissions;
sibling domains regime-detection and external-sourcing likewise exhausted). New free-data candidates
face a **raised domain gate ahead of the per-candidate gate**. This is a bar-ruling — a classification
against that gate — **not** a probe: nothing here is run, simulated, or pulled.

## §4 — Falsifiable hypothesis

**H:** LETF EOD-rebalance flow *clears the free-data domain bar* — i.e. it is a mechanism the free
searches could not access (paid/exogenous data), or it relaxes a binding venue wall, or it covers a
dated live incident the book failed. **Falsifier:** if the rebalance signal is **derivable from public
data** (issuer-published daily AUM + public index return + known leverage → mechanical rebalance
direction and size), it is a *free-data* mechanism → it lands squarely inside the tail-exhausted
free-data domain and clears **none** of the three re-proposal routes, so H is **falsified**
(reject-at-bar). H would instead be *supported* only if exploiting it demonstrably requires
**paid NDX-native order-flow** with an orthogonal, non-decayed edge, or a **new venue class**, or a
**dated live incident** — none of which the advisor's framing supplies.

**Adjudication:** the rebalance direction and magnitude are fully reconstructable from public AUM +
public returns + published leverage. The signal is **free-data**. → **Falsifier fires.**

## §5 — Forbidden moves

- **Admitting D2 past the free-data domain bar on mechanism plausibility alone.** The bar explicitly
  rejects "another free-data mechanism / a wider sweep / a different instrument / a longer panel" —
  the mechanism being *real* (it is) is not a clearance route. Reality ≠ orthogonal, non-decayed,
  bar-clearing alpha.
- **Treating the advisor's AUM figures as established** (~$117B Sept-2024; ~$198–201B / 754 funds
  mid-2026; ~$30B 2009). These are advisor claims — `verify-source` before any load-bearing use.
  They are **not** load-bearing for *this* verdict (the free-data classification is decisive
  regardless of magnitude), so no verification is spent here; they would need verifying only if the
  ruling were ever escalated on a cleared route.
- **Running or simulating anything** — including a cost-law pre-screen. The domain bar exists
  precisely to *avoid* spending even a cheap probe on an exhausted-domain free-data candidate; a
  pre-screen here would be the exhausted move.
- **Re-routing to the OHLCV raised-bar's "order-flow modality #2" sanction.** That sanction is for
  *microstructure/order-flow* re-entry (Avenue A's territory, scoped separately); LETF-rebalance
  flow is a *public-AUM-derived* signal, not paid order-flow, so it does not inherit that sanction.

## §6 — Gate / verdict

**Verdict: FALSIFIED — reject-at-bar.** LETF EOD-rebalance flow is a **free-data exogenous mechanism**
in the tail-exhausted free-data 5th-leg domain. It clears **none** of the three re-proposal routes:

| Route | LETF EOD flow | Cleared? |
|---|---|---|
| Paid / exogenous data the free searches could not access | signal = public AUM + public return + known `L` | **No** — free-data |
| A new venue class relaxing a *binding* wall | trades ES/NQ on the same futures-prop venue | **No** |
| A dated live incident the book demonstrably failed | none cited | **No** |

Corroborating (not load-bearing) priors: the whole EOD-flow thread in this program reads
"real-mechanism / thin-or-redundant-and-decaying-alpha" (a4-flow scoping; advisor's own caveat that
these signals decay with adoption), and LETF rebalance flow is among the most widely front-run of
them. Disposition recorded in [`docs/rejected_candidates.md`](../../rejected_candidates.md) (this brief
is the Authoritative artifact).

**Re-open condition (mechanism-evidence, not parameters):** a fresh single-cut pre-registration on
**paid NDX-native rebalance/order-flow** showing an edge that is *both* orthogonal to the incumbent
book and non-decayed; **or** a new venue class; **or** a dated live incident the existing book failed
that this leg would have covered. NOT a free-data re-run, a magnitude re-estimate, a different
index/leverage tier, or a longer panel.

## §7 — Forked questions

- None opened. A reject-at-bar closes the direction; the re-open bar (§6) is the only re-entry.
  (Had the verdict been RESOLVED/admit, a cost-law-pre-screen Pre-Q would be forked here.)

## §10 — Audit hooks

```bash
# The domain bar this ruling is judged against:
rg -n "Domain-level tail-exhaustion raised bars" docs/rejected_candidates.md
# After recording, the rejected entry + its concept-intake comment must be present:
rg -n "leveraged-etf-eod-rebalance-flow|leveraged/inverse-ETF EOD" docs/rejected_candidates.md
# This brief is the Authoritative artifact the entry points to:
test -f docs/briefs/programs/2026-07-24-d2-letf-eod-flow-ruling.md && echo AUTHORITATIVE_OK
```

## Verification

§0 cites concrete repo paths ✓ · §4 states `H:` + falsifier and adjudicates it ✓ · §5 lists moves
genuinely tempting this ruling (admit-on-plausibility; trust the AUM figures; run a "cheap" probe) ✓ ·
§6 binary verdict (FALSIFIED) with the three-route table ✓ · §10 runnable ✓ · doctrine-connected
(free-data domain bar, §1) ✓.
