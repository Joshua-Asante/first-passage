# MSL-S4 Stage-1 — MGC expiry-OI-strike convergence (pre-G0)

**Status:** `STAGE-1 PASS` · **B4 GO paid 2026-08-21** · G0 [`PREREG_G0.md`](PREREG_G0.md) **FROZEN** ·
Explore-confirm **DEFERRED BY OPERATOR OVERRIDE** (no market-data access this session) · Pine
**authored CC-solo** — [runbook](RUNBOOK.md) · **$0 · K=0** · Step-4 cheap falsifier **filled
2026-08-21 addendum** — [`NOT DECISIVE`](_cheap_falsifier_expiry_oi_strike_convergence_2026-08-21_LOG.md)
· Explore-confirm **run 2026-08-21** —
[`AMBIGUOUS-HOLD`](_explore_confirm_2026-08-21_LOG.md) (negative-signed, FLIP-FAIL; not
literally FALSIFIED under the frozen gate)
**Card:** MSL-S4 · instrument **MGC** · mechanism **`expiry-oi-strike-convergence`** (NEW)
**Parent:** [MSL charter](../../../../docs/spec/2026-08-12-msl-manual-sourcing-loop-charter.md) steps
1–4 · [E1 HOLD closure](../../../../docs/briefs/closures/MSL-S7-closure-resolved-e1-hold.md)
(discharged by this card) · [WHO-track notice](../../../../docs/notes/notice/N-2026-08-14-msl-who-track.md)
(the estate-wide sweep this card's WHO sits outside of)
**Sourcing:** this WHO was named by a dedicated cross-lane search (databento data-mining lane —
blocked, no environment data access; literature-harvest lane; manual gap-hunt lane; a fourth
focused verification pass resolved a live disagreement between the literature and manual lanes
over whether this construct inherits an already-dead sibling's kill). Not part of the original
MSL first/second slate.

---

## Freeze (zero data contact)

| Field | Frozen value |
|---|---|
| Reference class | Highest-open-interest strike on the parent (GC) options chain, published by CME (Options Settlement Tool / OI Heatmap / Daily Bulletin) |
| Direction | Converge — long if price below the strike, short if above; entry only when displaced from the strike by ≥ a declared threshold |
| Window | Armed only inside a declared pre-expiry session window (design parameter, e.g. final 1–3 sessions before a listed weekly/monthly Gold options expiry) |
| Stop / exit | Technical (ATR-scaled swing level), not mandate-derived; session-flat by **16:45 ET** (Tradeify Select verified deadline) |
| Cadence | k=1; first valid signal per **expiry event**, not per session |
| Not chosen | Any construct requiring an assumption about unobservable dealer gamma *sign* (the correctly-dead sibling — see rejected-nearest below) |

**CONFIRM window:** not yet named — Explore-confirm is deferred this session (see §Deferred-step
disclosure below), so no IS/CONFIRM partition has been read or reserved against real data.

**Rejected nearest classes** (also in `MECHANISMS.md`):
- Directional dealer-gamma-sign forecast (informal, no id) — DEAD, not reopened: sign is
  unobservable, so direction is never entailed (BE1 — same failure as the FX 10:00 NY option cut
  and the NAS100 `regime-overlay` dealer-gamma gate). This class's direction is read directly off
  price-vs-published-strike instead, which is always observable — the load-bearing distinction.
- `london-range-failed-extension-fade` — **FALSIFIED on this exact instrument (MGC)**, the
  sharpest honest adjacency. Distinct data-generating process: session price-action level (every
  session) vs. published options-positioning level (only near a listed expiry).
- `pdh-pdl-failed-break-reclaim` / `overnight-range-failed-extension-fade` — same MR-at-level
  family, different reference clock; same distinction as above.
- `event-window-reversal` — scheduled-release direction is itself uncertain a priori; this
  construct's direction is deterministic given observable displacement.
- `regime-overlay` — a sizing/deploy gate on inferred regime state; this construct is an
  entry-role trigger.

---

## Cost basis (Rule 0)

Tradeify Select 100K Metals: `firm_rules.py` comment pin **MGC=$1.06**/side · tick_value **$1.00**
· 1 tick/side slip (same fade-spec RT convention this program already uses):

`RT = 2×$1.06 + 2×$1.00 = $4.12` · 4× hurdle = **$16.48**/contract/trade.

**Design point:** k=1 contract · stop 15 pts (ATR-scaled illustrative) · target 30 pts (rr=2). Real
win-rate `p` is unmeasured — not computed or invented (§Step 3).

---

## Step 2 — Dedup + door-check (executed)

### Cell consult (raw, run this session after declaring the id)

```
$ python scripts/instrument_profiles.py build
instrument_profiles: wrote ops/instruments/PROFILES.md + ops/instruments/profiles.json (27 ledger(s))

$ python scripts/instrument_profiles.py cell MGC expiry-oi-strike-convergence
=== MGC x expiry-oi-strike-convergence ===
ledger: ops/instruments/MGC.md
verdict: untested — no prior on this cell.
BINDING BAR: free-data-5th-leg-snag-closed-2026-07-01 -> ../../docs/rejected_candidates.md
K bank: read ../../discovery_manifests/ — never trust a snapshot.
prior: Third-leg E-K elimination is void as a gate after K-bank ADR; large disclosed bank remains
  a Req-3 fact, not an inherited kill. DISC-CAMP-0 history is disclosure, not re-litigation. [#G1]
```

### BINDING BAR answer

| Bar / domain item | Route answer |
|---|---|
| `free-data-5th-leg-snag-closed-2026-07-01` | **CLEAR via R-FRAMING §2.1** — identical resolution MSL-C2 already used for this exact bar on this exact ledger (`ops/instruments/MGC.md` SESSION LOG, 2026-08-12b). Tradeify-native survival construct sits outside the free-data 5th-leg SNAG scope; this card is not a portfolio-expansion candidate. Inherited, not re-argued. |

### Dedup `rg` (mechanism family, not instrument) — pasted, executed this session

```
$ rg -n -i "\bpin\b|pinning|expiry-cluster|expiry.cluster|pin.risk" \
    docs/rejected_candidates.md lab/CATALOG.md ops/instruments/MECHANISMS.md
docs/rejected_candidates.md:550: (unrelated — "re-pin to a newer BAR EXPORT panel", a data-panel
  repoint, not a mechanism)
# Zero hits for a pin/pinning/expiry-cluster mechanism class.

$ rg -ni "gamma|dealer.?hedg|options?.dealer|delta.?hedg|vanna|charm|open.interest.*strike|OI.by.strike" \
    docs/rejected_candidates.md lab/CATALOG.md ops/instruments/MECHANISMS.md
docs/rejected_candidates.md:379-402  (Q-ORB-GEX-1 dealer-gamma-sign regime-gate + sibling
  term-spread-regime-gate — NAS100, SPX cross-index proxy, DIRECTIONAL forecast construct, the
  correctly-dead sibling this card does not reopen)
ops/instruments/MECHANISMS.md:308+  (this card's own new section — expected, not a collision)
# No hit for options-dealer/OI-by-strike on any metals or energy instrument outside this card.

$ rg -ni "GC\.OPT|MGC.*option|CL\.OPT|MCL.*option|weekly.gold.option" \
    docs/rejected_candidates.md lab/CATALOG.md ops/instruments/MECHANISMS.md ops/instruments/*.md
(no output — zero hits anywhere in the ledger tree)
```

**Confirmed:** no `pin`/`pinning`/`expiry-cluster` class exists in the registry, and no
options-OI-by-strike construct has been proposed, scored, or killed for MGC/MCL under any name.
Genuinely un-walked ground. (Re-derives the same result three independent research lanes reached
this session, using their own independently-run commands — see the sourcing-lane note above.)

### Adjacencies (not bars)

- `Q-ORB-GEX-1` / term-spread-regime-gate (NAS100) — both **directional sign-forecast**
  constructs, both DEAD on `G-regime-orthogonality` and era-confound respectively. Neither is this
  card's construct (convergence-toward-a-published-level, sign read off observable displacement,
  not assumed dealer positioning) — adjacency, not a bar.
- `london-range-failed-extension-fade` (MSL-C2, MGC) — FALSIFIED. Named explicitly above as the
  sharpest honest adjacency, not smoothed over: both are MR-at-a-level shapes on the same
  instrument. Distinguished by data-generating process, not by resemblance-avoidance.

---

## Step 3 — $0 screens at RT $4.12 (three kill limbs)

| Limb | Number | Gate | Verdict |
|---|---|---|---|
| cost-law | gross/trade = **$300** (30 pts × $10/pt) vs 4×RT **$16.48** | gross/trade ≥ $16.48 | **PASS** |
| payability | all-win day (k=1) = **$300** | ≥ $200 | **PASS** |
| survival | all-lose day (k=1) = **$150** | ≤ $750 | **PASS** |

Disclosures (non-gating): these three screens were never expected to be the discriminator for a
$10/point instrument — Req 1a's four clauses and the delete/flip test were (see
[`PREREG_G0.md`](PREREG_G0.md) §Req-1a for the full clause-by-clause record). No `p` was invented
to compute an implied-SR figure.

---

## Step 4 — Cheap falsifier

**NOT AVAILABLE this session** (record as of G0 freeze, 2026-08-21, unchanged below). A cheap
falsifier requires touching real price/OI data (even a generous, parent-side 5-minute check), and
this session's environment has no Databento API key and no cached market-data panel on disk
(`core/data/bar_data/` and `core/data/tv_exports/cme/` contain only manifests, not bytes —
vendor-licensed CSVs are gitignored per the repo's public-clone posture). This is the same
environmental block that stopped the databento data-mining sourcing lane outright. **Disclosed as
a gap, not silently skipped** — this is one of the two things the operator explicitly elected to
proceed without (the other being Explore-confirm; see [`PREREG_G0.md`](PREREG_G0.md)).

**Addendum, 2026-08-21 (later same day, separate local environment with `DATABENTO_API_KEY`
configured):** the gap above is now filled —
[`_cheap_falsifier_expiry_oi_strike_convergence_2026-08-21_LOG.md`](_cheap_falsifier_expiry_oi_strike_convergence_2026-08-21_LOG.md).
**Verdict: `NOT DECISIVE`** — a generous/informal delete-test analogue (7 completed OG monthly
cycles, $0 cost): arm-window (3 sessions pre-expiry) and control-window (matched length,
non-expiry) convergence toward the max-OI strike both land at 4/7 — identical rate, no
differential signal. This is **not** the pre-registered Explore-confirm (§4 below still applies
unchanged: no IS/CONFIRM partition reserved, no significance test, monthlies only). Does not kill
the card, does not clear it — full Explore-confirm remains the owed step before any TV/live
build-out.

**Addendum, 2026-08-21 (Explore-confirm, under `EXPLORE_GO.md` ISSUED 2026-08-21):** the owed
Explore-confirm ran — [`_explore_confirm_2026-08-21_LOG.md`](_explore_confirm_2026-08-21_LOG.md).
75 completed weekly+monthly OG cycles (IS window 2024-01-01→2025-03-31; CONFIRM 2025-04-01→
2025-09-29 never read). **Verdict: `AMBIGUOUS-HOLD`** — IAAFT-surrogate `p_upper=0.5724` (real
mean displacement reduction −5.52pts sits at the 42.8th percentile of the null, i.e.
indistinguishable from generic autocorrelated price dynamics); DELETE weakly PASSes (real strike
less-divergent than a generic sham level, both still negative); **FLIP FAILs** (divergence beats
convergence empirically — the construct's own directional claim does not hold up). Substantively
close to dead (wrong sign + FLIP-FAIL), though the frozen `p_upper > 0.95` FALSIFIED line isn't
literally crossed. `K_intrinsic` unchanged; CONFIRM untouched; formal card disposition left to
operator review.

---

## Verdict

**STAGE-1 PASS** + operator **B4 GO (2026-08-21)** → G0 [`PREREG_G0.md`](PREREG_G0.md) **FROZEN**.
Explore-confirm (charter step 5a) deferred by operator override (data-access gap). Pine authored
CC-solo this same session (charter step 6) — [`RUNBOOK.md`](RUNBOOK.md). No K spend. No TV seat yet.

**Next:** operator TV backtest (charter step 7) per the runbook, understanding the deferred
Explore-confirm has since run (addendum above) and landed `AMBIGUOUS-HOLD` — leaning dead
(negative-signed effect, FLIP-FAIL), not a clean kill under the frozen gate's own literal
threshold. Step-4 cheap falsifier filled 2026-08-21 — `NOT DECISIVE` (superseded in design by the
Explore-confirm's IAAFT null, per `EXPLORE_GO.md`). Neither TV nor this Explore-confirm result
substitutes for the other (§5 forbidden moves) — but the operator should weigh the Explore-confirm
result before spending further effort on a TV seat or any build-out.
