**Theme:** c1
# Third-leg instrument feasibility map

**Status:** **ACTIVE** -- Stage 1 discharges the contract-specs limb; Stage 2 measured sigma + tau_max for all four (RESULTS_stage2.md)
> ⚠ **K COLUMNS SUPERSEDED AS DOCTRINE 2026-08-04 (claim-alignment M45).**
> The table below computes `K_eff = K_intrinsic + K_banked(family)` — the rule in force
> 2026-07-27. Under ADR [`2026-08-04-family-k-bank-disclosure-not-gate`](../../../docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md)
> (`K_eff = K_intrinsic`) **every row screens at `K_eff` 1 / DSR floor 0.650 and Clause K
> passes on all eight**, so the **E-K (MGC)** and **E-KCAP (MNQ, MES)** eliminations do
> **NOT** survive and `{M2K, M6A, MYM, MCL}` is **not** the current survivor set.
>
> Body retained **unregenerated** as the record of the prior regime.
> `lab/discovery/instrument_map.py::k_eff` is deliberately left on the old formula for
> closed-study reproducibility — **do not re-run it expecting current floors.**
> **Edit no table cell.**



**Verdict:** `BAND NON-EMPTY (STAGE-1 — τ_max UNMEASURED)` -- Stage 1 only (free, exact, no price data).
**Basis:** daily-$ per contract at the $100K Tradeify Select basis.
**Inputs (`specs.json` meta):** σ cap **$125.00**/contract/day · commission **$0.91**/side · DSR Cap **1.0** · generated **2026-07-27**
**Screens; admits nothing.** Scope: Stage 1 discharges the contract-specs limb; Stage 2 measured sigma + tau_max for all four (RESULTS_stage2.md).

**Clause-N power floor** -- primary shared panel (reserved-IS, N=484): **0.0891** · full-OOS (N=749): 0.0716. Per-row floors below use each instrument's OWN panel.

**§5.2 falsifier:** ranking flip between 1-tick and 2-tick = **no**

| Symbol | Group | K bank | K_eff | DSR floor | RT 1t | RT 2t | cost-tax 1t r=1 | cost-tax 1t r=2 | cost-tax 2t r=1 | N (own panel) | power floor (own panel) | Verdict | Flags |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| MYM | Equity Index | 1 | 2 | 0.85 | $2.32 | $2.82 | 0.0742 | 0.1485 | 0.0902 | 484 | 0.0891 | **SURVIVOR** | S4-LONG-ONLY |
| M2K | Equity Index | 0 | 1 | 0.65 | $2.32 | $2.82 | 0.0742 | 0.1485 | 0.0902 | 484 | 0.0891 | **SURVIVOR** | S4-LONG-ONLY |
| MCL | Energy | 1 | 2 | 0.85 | $2.82 | $3.82 | 0.0902 | 0.1805 | 0.1222 | 251 | 0.1237 | **SURVIVOR** | FLAG-POWERBIND |
| M6A | Currencies | 0 | 1 | 0.65 | $2.82 | $3.82 | 0.0902 | 0.1805 | 0.1222 | 484 | 0.0891 | **SURVIVOR** | FLAG-COSTBIND |
| M6E | Currencies | 1 | 2 | 0.85 | $5.92 | $5.92 | 0.1894 | 0.3789 | 0.1894 | — | — | E-COST | -- |
| MGC | Metals | 3177 | 3178 | 2.05 (past pinned ladder) | $2.82 | $3.82 | 0.0902 | 0.1805 | 0.1222 | — | — | E-K | -- |
| MNQ | Equity Index | 2 | 3 | 0.98 | $2.32 | $2.82 | 0.0742 | 0.1485 | 0.0902 | — | — | E-KCAP | -- |
| MES | Equity Index | 2 | 3 | 0.98 | $3.07 | $4.32 | 0.0982 | 0.1965 | 0.1382 | — | — | E-KCAP | -- |

## Reading this table

- **cost-tax** = minimum per-trade edge as a fraction of the R1-capped daily sigma. `r` is round-trips per session; a bare figure is ambiguous by a factor of `r`.
- **Verdict token.** `BAND NON-EMPTY (STAGE-1 — τ_max UNMEASURED)` is a Stage-1-only token. It fires on "≥1 instrument survived elimination", which is strictly weaker than the design §5.1 pre-registration ("≥1 survivor whose τ_max is large enough to host an expressible mechanism") -- τ_max is not measured until Stage 2. The unqualified `BAND NON-EMPTY` stays reserved for that.
- **N (own panel)** = Slot-1 sessions from this instrument's own sourced `panel_start` to 2024-01-01. `—` where the row is eliminated and N was never probed. N does **not** enter E-K / E-KCAP / E-COST, so the survivor set is independent of it.
- **E-K** = Clause K FAILS (floor > Cap 1.0; no seed possible). **E-KCAP** = Clause K passes, but one seed remains at the 0.98 bar -- a recorded election, not a ratified gate.
- **FLAG-COSTBIND** = cost-tax exceeds the row's OWN power floor, so COST binds before power. This reverses the parent spec's assumption that T2 binds a thin slot.
- **FLAG-POWERBIND** = cost-tax clears the shared primary-panel floor but NOT the row's own (shorter) panel floor -- power binds first, and a universal-N read would have mislabelled the row `FLAG-COSTBIND`.
- **S4-LONG-ONLY** = Equity Index group; must be long-only against the long-only c1 book.
- **E-VENUE did not fire** -- all eight symbols are on the Tradeify product set.

## What this does NOT establish

A survivor is not admissible. It has cleared an instrument-level pre-screen only. **R1 is measured in Stage 2** (windowed sigma + τ_max for all four survivors -- see `RESULTS_stage2.md`), not at Stage 1; nothing on this page verifies it. T2/T3/T4/T5 and the whole §7.4 mechanism limb are untouched. Stage 2 was gated on a cost dry-run and on cache coverage; **both are measured in the Phase B gate section below** -- `cache_coverage.py` owns the coverage figure and this generator deliberately does not restate it, so a Stage-2 pull cannot leave a stale number here.

> **Regeneration note.** Everything above this line is emitted by `python -X utf8 instrument_map.py > RESULTS.md` (Phase A). The Phase B gate section below is appended from `cache_coverage.py` + the recorded `estimate` probes and is **not** regenerated -- re-append it after any regenerate.

## Phase B gate (as measured 2026-07-27) -- SUPERSEDED 2026-07-28

> **Superseded 2026-07-28 — see [`RESULTS_stage2.md`](RESULTS_stage2.md). This pointer scopes the WHOLE section below, including its closing status paragraph.** Stage 2 has since been run: all four survivors sit at 100% cache coverage of their own IS windows and windowed sigma + τ_max are measured for each. The **measurements** recorded below are kept **byte-intact as the historical record** — the `$0.00` dry-run price, the `0/56` coverage *as measured 2026-07-27*, and the MCL 422 pre-inception caveat were each accurate when the gate ran. Every *forward-looking* statement in this section ("not started", "one open question remains", "until that decision") has been overtaken by events and is retained only as the record of what was true at the gate.

**Pre-2024 IS cache coverage: `0/56` chunks, every survivor (MYM, M2K, MCL, M6A).**
Measured 2026-07-27 via `cache_coverage.py` against the live `~/.databento_cache`
(284 files on disk, ~438 MB). Re-measured after `coverage()` was corrected to check
every `db_fetch` key variant, not just the fully-tagged one -- still `0/56`, so no
legacy untagged chunk was hiding. The only data already held for these legs
(MNQ/MYM 2025-06 -> 2026-07) sits *inside* the reserved ST-EH-1 2024+ holdout and is
therefore unusable here regardless of price.

**Dry-run price for `ohlcv-1m`: measured `$0.00`.** `db_fetch.py estimate` over the
**entire** MYM pre-2024 IS window `2019-05-06 -> 2024-01-01` (continuous `MYM.v.0`,
GLBX.MDP3, `ohlcv-1m`) returns **`$0.0000`** for **89,280,632 bytes / 1,594,297
records**. Full-precision `client.metadata.get_cost()` returns exactly `0.0`, not a
rounding artifact of the CLI's 4-decimal print. `ohlcv-1m` on GLBX.MDP3 is **covered
by the subscription**; the schemas that bill are `bbo-1s` / `tbbo` / `mbp-10` (see
the Q-COSTGEO-1/2/3 record).

**Therefore the §4.1 reserved-holdout choice stands unchanged and costs nothing.**
The reservation was adopted because it looked free. It *is* free: the schema Stage 2
needs prices at $0.00 over the whole reserved-IS window. The earlier reading — that
honouring the holdout "now costs a full paid pull", with an option to spend the
ST-EH-1 2024+ holdout instead — rested on a premise that measurement falsifies.
**Burning the reserved holdout to avoid a cost of zero is not on the table and never
was.** §4.1 is unamended.

**Per-chunk extrapolation:** `$0.0000 × 56 × 3 = $0.00` (MYM, M2K, M6A measured);
MCL not priceable on this chunk — see caveat below. The whole-window MYM estimate
above is the stronger of the two figures: it prices the full 2019-05-06 -> 2024-01-01
span in one call rather than extrapolating from a month.

**Caveat -- MCL pre-inception gap (unplanned finding, surfaced not guessed):**
`MCL.v.0` does **not** price on the reserved-IS chunk starting 2019-05-06 -- the
estimate call fails with `422 symbology_invalid_request: None of the symbols could be
resolved`, which is an *unobtained* number, not a `$0` quote. The identical symbol
resolves cleanly (also `$0.0000`) from 2021-08 onward, consistent with Micro WTI not
existing on Globex in mid-2019. Two consequences, both now carried in the table
above: MCL's true pre-2024 IS chunk count is **below 56 for reasons unrelated to
spend**, and its Slot-1 panel is **N = 251, not 484** — which is why its annotation is
`FLAG-POWERBIND`, not `FLAG-COSTBIND`. `panel_start = 2021-08-01` is the earliest
month verified resolvable; true inception may be marginally earlier, and a later
`panel_start` understates N and therefore *raises* the floor, so the pin errs
conservative.

**N is a Stage-2 prioritization fact, not a screen input.** `N` never enters E-K,
E-KCAP, or E-COST, so **the survivor set is unchanged** by the panel-start correction
— MYM, M2K, MCL, M6A, exactly as before. What changes is which wall each survivor
hits first.

**Reading the `$0.00` figure:** it is the measured API quote today, under the
account's current plan, for the coarse `ohlcv-1m` schema specifically. It is not a
claim about `mbp-10` / `mbo` / `tbbo` pricing (those bill), and it is not a guarantee
the quote holds at a later date. Report it as measured; re-verify with a fresh
`estimate` call before any `pull`.

**Status AT THE GATE (2026-07-27) — historical, superseded; see the pointer at the top
of this section.** Stage 2 was **not started**. With the price measured at zero, the
no-buy-before-survivor rule was **not engaged** — that rule gates *spend*, and there was
none to gate. One open question remained, and it was not about money:

1. **Whether to spend operator time on Stage 2.** Stage 2 costs attention, not
   dollars: the pull, windowed-σ measurement, and τ_max derivation for four survivors,
   against the 07-28 B7/M1 attention block. That is an operator call. Declining it
   ships the map at Stage 1 as it stands; taking it opens over survivors only.

**Resolved 2026-07-28: it was taken.** The pull ran to 100% coverage on every survivor's
own IS window and Stage 2 measured the sigma surfaces and τ_max —
[`RESULTS_stage2.md`](RESULTS_stage2.md) carries the coverage figures, the measurements,
and its own (still-qualified) Stage-2 verdict token. The Stage-1 verdict above remains
the Stage-1 verdict: it is not restated, revised, or promoted by that result.
