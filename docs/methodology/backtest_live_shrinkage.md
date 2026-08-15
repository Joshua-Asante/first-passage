# Backtest → live shrinkage convention

**Status:** methodology **convention** (an ex-ante planning prior). **NOT a gate, NOT
a sizing constant, and NOT a change to any locked risk %.** It sets an *expectation*
for what live performance a validated backtest should be underwritten to deliver; it
does not by itself resize anything. Any actual sizing haircut at a go-live is a
separate, gated decision owned by `docs/methodology/strategy_lifecycle.md` (authorization
ladder) + operator GO/NO-GO — never applied silently from this page.

Rationale: `docs/methodology/references/statistics-of-tradable-anomalies.md` Domain 5
(decay is the base case) + Domain 8 (Bayesian admission-to-live bridge).

---

## The base rate

Edges are wasting assets with unknown half-lives — part sampling illusion, part
arbitraged-away. McLean–Pontiff (2016), across 97 published anomalies, measured the
two components:

- **≈ −26% out-of-sample** — the pure overfitting/selection share (the edge was
  partly noise the backtest fit).
- **≈ −58% post-publication** — adding the crowding share (others trade it once it's
  known).

The installed prior: **plan for live to retain roughly 30–70% of backtest edge**
(Sharpe / expectancy), *before* any strategy-specific divergence is even considered.
Expecting ~100% of backtest is the single most common way a validated system still
disappoints in production.

Two structural modifiers move a specific strategy within that band:

- **Search intensity ↑ ⇒ retain less.** A heavily-mined edge (high K, Domain 4) is a
  more upward-biased estimate, so shrink harder. A pre-registered, mechanism-first,
  low-K edge sits nearer the top of the band. This is why the discovery pipeline's K
  ledger and DSR feed the sizing prior, not just the pass/fail gate.
- **Capacity ↓ ⇒ decay slower.** Effects too small for institutional size to harvest
  (micro-scale, short-horizon, high-friction) crowd slower post-discovery — the
  marginal arbitrageur isn't paid enough to come. One of the few structural advantages
  of trading small: our micro/CFD-scale edges should sit nearer the *top* of the
  retention band on the crowding axis, even as the overfitting axis still applies.

## The convention (ex-ante, at underwriting)

When projecting a validated backtest forward to a go-live decision:

1. **State the retention assumption explicitly** in the pre-registration / admission
   doc — e.g. "underwritten to X% of backtest expectancy," with X justified by the
   two modifiers above. An unstated assumption defaults to 100%, which is wrong.
2. **Size on the shrunk, lower-confidence-bound edge**, not the point estimate — the
   Domain-6 practice (every backtest edge is upper-biased; size on a lower quantile).
   Fractional sizing that steps up only as live trade count accumulates is the
   sequential version (the lifecycle's ramp; automation moves authorization *down*
   only, never up — a ramp-up is an operator decision).
3. **Carry it as a falsifiable expectation, not a promise.** The reconciliation is
   looking for where in the 30–70% band the strategy actually lands — it should not be
   surprised that live < backtest; it should have said so first.

## Relationship to ECR (ex-post, the falsifier)

The **edge-captured ratio** (ECR = realized / counterfactual-backtest-PnL over the
same window; floor **0.70**; `ops/live_journal/` + PREREG-NAS-ECR-1) is the *ex-post*
instrument and is a **different quantity** from this ex-ante prior — do not conflate:

| | Shrinkage convention (this page) | ECR (`live_journal`) |
|---|---|---|
| When | Ex-ante, at underwriting | Ex-post, after fills accrue |
| Measures | *Expected* live/backtest edge retention (decay + crowding) | *Realized* execution fidelity vs the same-window backtest counterfactual |
| Divides out | nothing — it is the whole edge | edge magnitude (faithful execution of a *decaying* edge keeps ECR ≈ 1) |
| Role | planning prior → sizing input | falsifier floor → WATCH/kill trigger |

So a strategy can be **executed faithfully (ECR ≈ 1) and still decay** — ECR would not
catch that; the shrinkage prior is what set the expectation that live edge < backtest
in the first place, and the lifecycle's rolling-PF decay trigger (Call-1) is what
catches the decay. They are complementary, not substitutes. (This is the same
Q-DECAY-1 lesson: ECR is execution-fidelity, not a decay detector.)

## Where it applies — and where it does NOT

- **Applies now to:** the **Aegis→M6J** go-live underwriting (the sole active scale
  lane; go-live is a separate gated decision) and any discovery-campaign survivor
  exiting Stage-8 into `strategies-never-locked` admission. The parent→micro proxy
  discipline already reserves the native-micro era as OOS; this convention is the
  *sizing* counterpart — even a micro-OOS-validated edge is underwritten below its
  backtest point estimate.
- **Does NOT apply to / does NOT touch:** the locked 4-strategy CFD portfolio's
  allocations, `dd_protection`, the MC anchor (99.83/0.17/4.37), or any Pine constant.
  Those are LOCKED at the parameter axis; this page is a planning prior for *new*
  live underwriting, not a retroactive haircut on the locked book. It introduces no
  number that `validate_params` or the MC pins would see.

## Related

- `docs/methodology/references/statistics-of-tradable-anomalies.md` — Domains 5, 6, 8.
- `docs/methodology/strategy_lifecycle.md` — the authorization ladder + ramp that any actual de-risk flows through.
- `docs/methodology/1r_estimation.md` — the Striker-specific expected live<backtest divergence sits *inside* this program-level prior.
- `docs/spec/PREREG-NAS-ECR-1-live-edge-capture.md` + `ops/live_journal/` — the ECR falsifier machinery (ex-post).
