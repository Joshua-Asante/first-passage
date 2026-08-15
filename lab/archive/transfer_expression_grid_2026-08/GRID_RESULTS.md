# Q-TXG-1 — transfer/expression grid (Block 1 compile)

**Status:** CLOSED — FALSIFIED-at-walls (operator A, 2026-08-12) — Block-1 compile record retained; H_A OPEN below is the *compile-time* verdict, superseded for election by the lane ruling. Authoritative disposition: [RESULTS.md](RESULTS.md) · [packet](lab/archive/../../../docs/briefs/Q-TXG-1-ha-reargument.md)
**Date:** 2026-08-11 · **Runner:** [run_grid_compile.py](run_grid_compile.py) · **Raw:** [GRID_RESULTS.json](GRID_RESULTS.json)
**Cost: $0.00 · K=0 · no manifest · no data pull · no network · no PnL/return reads.**
Design: docs/superpowers/specs/2026-08-11-transfer-expression-grid-design.md ·
PREREG: [PREREG.md](PREREG.md)

## §1 Why this exists
Generation lanes closed in sequence (census, ENV-1 NULL, MCLTAS FALSIFIED, dense-1m AMBIGUOUS/STOP).
The transfer lane has validated outputs on record but was never systematized — walls discovered mid-
campaign. This compiles the 4×7 grid at $0 against ENV-1 envelopes and the citation-chain mechanism
constants so election aims at survivors, not ghosts.

## §2 The compiled grid (28 cells)

**Basis:** Q-TXG-1 Block 1 — Tradeify_Select_100K eval — 4 mechanisms × ENV-1 7-micro pool — walls W-DEDUP/W-VENUE/W-CAP/W-COST (W-CADENCE/W-REGIME/S7 disclosure) — envelope.py owner for cell arithmetic — $0/K=0/no PnL reads

**DSR floors (K=1/2/3):** 0.65 / 0.85 / 0.98

| mech | sym | transfer | stop_raw | stop_map | cost_tax | qty | verdict |
|---|---|---|---:|---:|---:|---:|---|
| guardian | MNQ | cross-underlying | — | UNSCR | — | 4 | OPEN |
| guardian | MYM | cross-underlying | — | UNSCR | — | 4 | OPEN |
| guardian | MES | cross-underlying | — | UNSCR | — | 1 | OPEN |
| guardian | MGC | same-underlying | — | UNSCR | — | — | PARKED(b8) |
| guardian | M2K | cross-underlying | — | UNSCR | — | 4 | OPEN |
| guardian | MCL | cross-underlying | — | UNSCR | — | 2 | OPEN |
| guardian | M6A | cross-underlying | — | UNSCR | — | 2 | OPEN |
| striker | MNQ | cross-underlying | 218.45 | 160 | 0.030R | 8 | OPEN |
| striker | MYM | same-underlying | — | UNSCR | — | — | WITHDRAWN(F1) |
| striker | MES | cross-underlying | — | UNSCR | — | 3 | OPEN |
| striker | MGC | cross-underlying | — | UNSCR | — | 4 | OPEN |
| striker | M2K | cross-underlying | — | UNSCR | — | 8 | OPEN |
| striker | MCL | cross-underlying | — | UNSCR | — | 4 | OPEN |
| striker | M6A | cross-underlying | — | UNSCR | — | 4 | OPEN |
| striker_nas100 | MNQ | same-underlying | — | UNSCR | — | — | WITHDRAWN(F1) |
| striker_nas100 | MYM | cross-underlying | 60.82 | 80 | 0.060R | 9 | OPEN |
| striker_nas100 | MES | cross-underlying | — | UNSCR | — | 1 | OPEN |
| striker_nas100 | MGC | cross-underlying | — | UNSCR | — | 2 | OPEN |
| striker_nas100 | M2K | cross-underlying | — | UNSCR | — | 4 | OPEN |
| striker_nas100 | MCL | cross-underlying | — | UNSCR | — | 2 | OPEN |
| striker_nas100 | M6A | cross-underlying | — | UNSCR | — | 2 | OPEN |
| aegis | MNQ | cross-underlying | — | UNSCR | — | 18 | OPEN |
| aegis | MYM | cross-underlying | — | UNSCR | — | 18 | OPEN |
| aegis | MES | cross-underlying | — | UNSCR | — | 7 | OPEN |
| aegis | MGC | cross-underlying | — | UNSCR | — | 9 | OPEN |
| aegis | M2K | cross-underlying | — | UNSCR | — | 18 | OPEN |
| aegis | MCL | cross-underlying | — | UNSCR | — | 9 | OPEN |
| aegis | M6A | cross-underlying | — | UNSCR | — | 9 | OPEN |

**H_A: OPEN**  (25 OPEN cells)

## §3 H_A verdict

**H_A: OPEN** (n=25 of 28). Verdict mix: OPEN 25 · WITHDRAWN(F1) 2 · PARKED(b8) 1. DEAD-by-wall (W-VENUE / W-CAP / W-COST) = 0.

UNSCREENABLE is a `stop_cell` / disclosure, not a separate verdict. PARKED/WITHDRAWN are excluded from OPEN. The only kill wall that fired is **W-DEDUP**: `striker×MYM` WITHDRAWN(F1), `striker_nas100×MNQ` WITHDRAWN(F1), `guardian×MGC` PARKED(b8). W-VENUE and W-CAP cleared the remaining 25; W-COST cannot fire without a mapped stop, and the two mapped cells cleared it.

Most OPEN cells are stop-unscreenable by design (no ATR-matched median on that instrument — 23/25 carry `stop_cell: UNSCREENABLE`). Two mapped-stop OPEN cells: **striker×MNQ** (160t, 0.030R) and **striker_nas100×MYM** (80t, 0.060R).

## §4 Per-OPEN-cell targets (numbers the port must beat)

Source: `GRID_RESULTS.json` `open_cells[]` (n=25). Dicts are the frozen `port_must_beat` payload.

| mech×sym | transfer_type | port_must_beat |
|---|---|---|
| guardian×MNQ | cross-underlying | `{"lifecycle": 1.0, "nsurv_ceiling_pct": 3.0, "risk_pct": 0.0034, "stop_cell": "UNSCREENABLE"}` |
| guardian×MYM | cross-underlying | `{"lifecycle": 1.0, "nsurv_ceiling_pct": 3.0, "risk_pct": 0.0034, "stop_cell": "UNSCREENABLE"}` |
| guardian×MES | cross-underlying | `{"lifecycle": 1.0, "nsurv_ceiling_pct": 3.0, "risk_pct": 0.0034, "stop_cell": "UNSCREENABLE"}` |
| guardian×M2K | cross-underlying | `{"lifecycle": 1.0, "nsurv_ceiling_pct": 3.0, "risk_pct": 0.0034, "stop_cell": "UNSCREENABLE"}` |
| guardian×MCL | cross-underlying | `{"lifecycle": 1.0, "nsurv_ceiling_pct": 3.0, "risk_pct": 0.0034, "stop_cell": "UNSCREENABLE"}` |
| guardian×M6A | cross-underlying | `{"lifecycle": 1.0, "nsurv_ceiling_pct": 3.0, "risk_pct": 0.0034, "stop_cell": "UNSCREENABLE"}` |
| striker×MNQ | cross-underlying | `{"cost_tax_r": 0.03, "env1_cell_verdict": "OPEN-CONDITIONAL(power)", "lifecycle": 1.0, "nsurv_ceiling_pct": 3.0, "qty_at_locked_risk": 8, "required_net_r": 0.03, "risk_pct": 0.007, "stop_ticks": 160}` |
| striker×MES | cross-underlying | `{"lifecycle": 1.0, "nsurv_ceiling_pct": 3.0, "risk_pct": 0.007, "stop_cell": "UNSCREENABLE"}` |
| striker×MGC | cross-underlying | `{"lifecycle": 1.0, "nsurv_ceiling_pct": 3.0, "risk_pct": 0.007, "stop_cell": "UNSCREENABLE"}` |
| striker×M2K | cross-underlying | `{"lifecycle": 1.0, "nsurv_ceiling_pct": 3.0, "risk_pct": 0.007, "stop_cell": "UNSCREENABLE"}` |
| striker×MCL | cross-underlying | `{"lifecycle": 1.0, "nsurv_ceiling_pct": 3.0, "risk_pct": 0.007, "stop_cell": "UNSCREENABLE"}` |
| striker×M6A | cross-underlying | `{"lifecycle": 1.0, "nsurv_ceiling_pct": 3.0, "risk_pct": 0.007, "stop_cell": "UNSCREENABLE"}` |
| striker_nas100×MYM | cross-underlying | `{"cost_tax_r": 0.06, "env1_cell_verdict": "OPEN", "lifecycle": 1.0, "nsurv_ceiling_pct": 3.0, "qty_at_locked_risk": 9, "required_net_r": 0.06, "risk_pct": 0.0037, "stop_ticks": 80}` |
| striker_nas100×MES | cross-underlying | `{"lifecycle": 1.0, "nsurv_ceiling_pct": 3.0, "risk_pct": 0.0037, "stop_cell": "UNSCREENABLE"}` |
| striker_nas100×MGC | cross-underlying | `{"lifecycle": 1.0, "nsurv_ceiling_pct": 3.0, "risk_pct": 0.0037, "stop_cell": "UNSCREENABLE"}` |
| striker_nas100×M2K | cross-underlying | `{"lifecycle": 1.0, "nsurv_ceiling_pct": 3.0, "risk_pct": 0.0037, "stop_cell": "UNSCREENABLE"}` |
| striker_nas100×MCL | cross-underlying | `{"lifecycle": 1.0, "nsurv_ceiling_pct": 3.0, "risk_pct": 0.0037, "stop_cell": "UNSCREENABLE"}` |
| striker_nas100×M6A | cross-underlying | `{"lifecycle": 1.0, "nsurv_ceiling_pct": 3.0, "risk_pct": 0.0037, "stop_cell": "UNSCREENABLE"}` |
| aegis×MNQ | cross-underlying | `{"lifecycle": 1.0, "nsurv_ceiling_pct": 3.0, "risk_pct": 0.015, "stop_cell": "UNSCREENABLE"}` |
| aegis×MYM | cross-underlying | `{"lifecycle": 1.0, "nsurv_ceiling_pct": 3.0, "risk_pct": 0.015, "stop_cell": "UNSCREENABLE"}` |
| aegis×MES | cross-underlying | `{"lifecycle": 1.0, "nsurv_ceiling_pct": 3.0, "risk_pct": 0.015, "stop_cell": "UNSCREENABLE"}` |
| aegis×MGC | cross-underlying | `{"lifecycle": 1.0, "nsurv_ceiling_pct": 3.0, "risk_pct": 0.015, "stop_cell": "UNSCREENABLE"}` |
| aegis×M2K | cross-underlying | `{"lifecycle": 1.0, "nsurv_ceiling_pct": 3.0, "risk_pct": 0.015, "stop_cell": "UNSCREENABLE"}` |
| aegis×MCL | cross-underlying | `{"lifecycle": 1.0, "nsurv_ceiling_pct": 3.0, "risk_pct": 0.015, "stop_cell": "UNSCREENABLE"}` |
| aegis×M6A | cross-underlying | `{"lifecycle": 1.0, "nsurv_ceiling_pct": 3.0, "risk_pct": 0.015, "stop_cell": "UNSCREENABLE"}` |

## §5 Dedup attestation (execute-time paste)

W-DEDUP used the frozen disposition map (PREREG F5). The consult below is attestation, not a live branch. First 80 of 86 `rg` matches (Block-1 compile, Task 5). All 7 `cell SYM placeholder` calls exit 2 (`FATAL: unknown mechanism 'placeholder'`). **M6A ledger EXISTS** — do not claim no-ledger. ENV-1 housekeeping: the missing-ledger FATAL is stale; this is not a silent skip.

### rg (first 80 lines)

Command (Windows: `rg` available; `head` replaced by Python slice of 80 lines; total matches=86):

```
rg -in "guardian|striker|aegis|MYM|MNQ|MGC|transfer" docs/rejected_candidates.md docs/pursuits/b1-aegis-6j-transfer-lane.md docs/pursuits/b2-striker-mym-reconstruction.md docs/pursuits/b8-guardian-mgc-transfer-lane.md
```

```
docs/pursuits/b1-aegis-6j-transfer-lane.md:1:# Aegis→6J transfer lane — PARK
docs/pursuits/b1-aegis-6j-transfer-lane.md:7:**Residuals:** v0.3 measured record (`lab/analysis/aegis/aegis_6j_transfer_2026-07-05/`, `aegis_6j_trail_tradeify_2026-07-29/`) — retained hot, no owner reassignment needed; stays with the lab CATALOG until re-entry or expiry
docs/pursuits/b8-guardian-mgc-transfer-lane.md:1:# Guardian→MGC transfer lane (R7) — PARK (PROPOSED)
docs/pursuits/b8-guardian-mgc-transfer-lane.md:4:> Phase-1 inventory omission (Guardian-MGC/R7 does not appear in the a1–e2 tables),
docs/pursuits/b8-guardian-mgc-transfer-lane.md:10:**re-entry:** a real GC1!/MGC1! bar-export is landed AND a fresh pre-registration is
docs/pursuits/b8-guardian-mgc-transfer-lane.md:18:record for this lane (unlike Aegis→6J's v0.3 panel)
docs/pursuits/b8-guardian-mgc-transfer-lane.md:19:**Test applied:** data-blocked — R7 granularity-floor work "needs a real GC1!/MGC1!
docs/pursuits/b8-guardian-mgc-transfer-lane.md:21:Survive/resource / no-venue-route test: MGC is venue-legal at the four
docs/pursuits/b8-guardian-mgc-transfer-lane.md:22:automation-friendly firms (`ops/instruments/MGC.md` `venue_tradable: true`)
docs/pursuits/b8-guardian-mgc-transfer-lane.md:26:item 3 + §3 · [`07-16 ADR`](lab/analysis/adr/2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md)
docs/pursuits/b8-guardian-mgc-transfer-lane.md:27:§2 item 1 · [`MGC ledger`](lab/archive/../ops/instruments/MGC.md) ACTIVE/OPEN · GSUB-1 Phase-1
docs/pursuits/b2-striker-mym-reconstruction.md:1:# Striker MYM reconstruction (S-MYM-ORC-02, TERMINAL lane) — PARK
docs/pursuits/b2-striker-mym-reconstruction.md:7:**Residuals:** `lab/analysis/striker/striker_mym_reconstruction_candidate1_2026-07/` — stays hot under lab CATALOG convention until re-entry or expiry
docs/rejected_candidates.md:5:This file is appended to at the close of any Pre-Q that closes FALSIFIED on strategy grounds, or at the close of a parent programme on SNAG-budget-exhaustion grounds (the Guardian-on-XAGUSD precedent below). New entries link to the closure artifact authoritative for the rejection.
docs/rejected_candidates.md:15:### Guardian-family strategy on XAGUSD (Silver)
docs/rejected_candidates.md:25:Guardian **Silver v1.0** BE-off variant (0.15% fair-weather) was *admitted* 2026-06-11 via an
docs/rejected_candidates.md:27:([`docs/briefs/2026-06-11-guardian-silver-v1-admission-override.md`](briefs/2026-06-11-guardian-silver-v1-admission-override.md)),
docs/rejected_candidates.md:33:`_BASE_RISK` has 4 keys, no silver). **Operator CLOSED Guardian Silver v1.0 — NOT ADMITTED
docs/rejected_candidates.md:78:**Closure basis:** cost **pre-screen** (the cheapest falsifier — **NOT** a full pre-registered Pre-Q) on the canonical Pepperstone 5m EURUSD feed (445,798 bars, 2020-06 → 2026-06, **n=1550 fix-days**). The gross post-fix reversal **reproduces the source paper's magnitude** (best cell +0.0455R ≈ ~2 bps mean post-fix move) and is correct-signed (long-EURUSD-post-fix net-positive across the grid = the paper's USD-reverses-after-fix). But the **best-of-grid break-even is 0.277 pip ≪ FXIFY ~0.8 pip all-in**: net R is negative in every (hold × stop) cell at ≥0.4 pip cost, and the verdict is **robust to the exact spread** (gross edge ≤0.055R even at zero cost). Confirms the paper's own "not easy to exploit once transaction costs are accounted for." Same cost-law wall as the USDCAD Aegis-MR transfer (0.097R @1.42×ATR) and the USOIL spike-fader.
docs/rejected_candidates.md:91:### Aegis-v4.3 mean-reversion template port on EURGBP
docs/rejected_candidates.md:93:**Rejection scope:** the direction (Aegis-v4.3 Bollinger-band mean-reversion template — BB 19/1.9 + ATR19 + break-even, long-only, 15m — ported to EURGBP) is rejected, not only a single parameter set. **Refuted pre-build at 5th-leg adversarial review** — no EURGBP panel was exported or run.
docs/rejected_candidates.md:96:**Authoritative artifact:** [`ops/instruments/EURGBP.md`](lab/analysis/ops/instruments/EURGBP.md) (ledger stub D1 + durable findings F1–F3); refutation basis cross-references [`ops/instruments/USDCAD.md`](lab/analysis/ops/instruments/USDCAD.md) (durable #1 + dead-list) and [`docs/audits/2026-05-28-aegis-v43-indicator-strategy-diff.md`](audits/2026-05-28-aegis-v43-indicator-strategy-diff.md):214.
docs/rejected_candidates.md:97:**Closure basis:** refuted on the EDGE & COST angle, all basis facts verified on disk. (1) **Cost geometry fails** — EURGBP is the lowest-volatility G10 cross (ATR(14) ~6 pips; 15m ATR a few pips), so an Aegis 1.42×ATR(15m) stop is *smaller in price* than USDCAD while spread is comparable (~0.6–1 pip + commission); by the USDCAD COST LAW (cost-in-R ∝ price/stop_dist), cost/R ≥ 0.097R — USDCAD measured exactly 0.097R round-trip at 1.42×ATR(15m) and already failed a 4×-cost-hurdle gate. After-cost PF≈2.0 is not credible. (2) **Direct precedent dead** — Aegis USDCAD v0.1 (the same mean-reversion transfer to a comparable cross) FAILED: n=245, PF 0.756, pervasive trend-impulse loss character, no hour/day/regime refuge. (3) **Edge-persistence-in-chop fails** — the H1 (2020–2023) window that must be survived contains the 2022 sterling crisis (sustained EURGBP move ~0.82→~0.90, mini-budget spike to ~0.923 on 26 Sep 2022), the strong-trend sub-regime where MR bleeds; our own Aegis/USDJPY had 2022 PF only ≈1.12.
docs/rejected_candidates.md:102:     rejection_reason="venue/cost-constraint + edge-failure: Aegis-v4.3 MR template port refuted PRE-BUILD at 5th-leg adversarial review 2026-06-21 (no EURGBP panel run). (1) Cost geometry: EURGBP lowest-vol G10 cross (ATR14 ~6 pips), 1.42xATR(15m) stop smaller in price than USDCAD, spread comparable -> cost/R >= 0.097R by the USDCAD COST LAW; USDCAD measured 0.097R RT @ 1.42xATR and failed a 4x-cost-hurdle gate -> after-cost PF~2.0 not credible (L-COST-GEOMETRY). (2) Direct precedent: Aegis USDCAD v0.1 (same MR transfer, comparable cross) FAILED n=245 PF 0.756, pervasive trend-impulse, no regime refuge. (3) H1 2020-2023 contains the 2022 sterling crisis (0.82->0.90, spike 0.923 on 26 Sep 2022) -> strong-trend sub-regime where MR bleeds; Aegis/USDJPY 2022 PF ~1.12. See ops/instruments/EURGBP.md."
docs/rejected_candidates.md:107:     falsifier_failed="adversarial-review refutation (no panel run): cost-law cost/R >= 0.097R (USDCAD-measured @ 1.42xATR, failed 4x-cost-hurdle) -> after-cost PF~2.0 not credible; direct precedent Aegis USDCAD v0.1 n=245 PF 0.756; H1 contains 2022 sterling-crisis trend (Aegis/USDJPY 2022 PF ~1.12)"
docs/rejected_candidates.md:109:     config_fingerprint="aegis-v4.3-port/EURGBP/15m/BB19@1.9/ATR19/SL1.42xATR/TPbasis+0.8ATR/BE(0.30/0.15)/long-only/feed=canonical-TV-CSV(NO PANEL RUN - refuted pre-build at adversarial review)" -->
docs/rejected_candidates.md:110:- **bollinger-band-mean-reversion on EURGBP** — rejected 2026-06-21 (venue/cost-constraint + edge-failure: Aegis-v4.3 MR template port refuted pre-build at 5th-leg adversarial review. EURGBP lowest-vol G10 cross → 1.42×ATR(15m) stop smaller than USDCAD, spread comparable → cost/R ≥ 0.097R by the USDCAD COST LAW (USDCAD measured 0.097R RT @ 1.42×ATR, failed 4×-cost-hurdle) → after-cost PF~2.0 not credible; direct precedent Aegis USDCAD v0.1 dead (n=245, PF 0.756); H1 contains the 2022 sterling-crisis trend (Aegis/USDJPY 2022 PF ~1.12)); ledger `ops/instruments/EURGBP.md` (no harness DispositionRecord; refuted pre-build, never intaked).
docs/rejected_candidates.md:129:- Aegis SHORT v0.1
docs/rejected_candidates.md:130:- Guardian-on-USOIL
docs/rejected_candidates.md:151:> `python scripts/instrument_profiles.py cell MNQ ict-liquidity` prints `BINDING BAR` and blocks),
docs/rejected_candidates.md:166:* the prose `### <heading>` directional entries above (e.g. *Guardian-family
docs/rejected_candidates.md:182:The four locked-book strategies (Guardian Gold v5.5 / XAUUSD, Striker DJ30 v4.5 /
docs/rejected_candidates.md:183:DJ30, Aegis USDJPY v4.3 / USDJPY, Striker NAS100 v1 / NAS100) are pinned in the
docs/rejected_candidates.md:235:**Closure basis:** free-data 2022-rates era-split (cheapest falsifier, NOT a full Pre-Q) on Yahoo `^TNX` (10Y) / `^FVX` (5Y) daily 2010-2026 — a daily proxy that tests the **regime/tail-co-occurrence mechanism**, the disqualifier. 2022 was a violent one-directional rates selloff (10Y 1.63%→3.88%, +2.25pp), so a range-fade was **short a relentless uptrend through the 2020-2023 H1 chop window** = the Aegis-USDJPY-2022 bleed mode. Canonical daily fade (z=(y−SMA20)/SD20, fade |z|≥1): **worst year 2022 (10Y −124bp / 5Y −116bp, hit 44%); H1 net-negative both tenors (Sharpe −0.31 / −0.47)** → K1 (tail co-occurrence) fires: the leg deepens the book's H1 co-drawdown rather than offsetting it. K2 (era-relabel) does not fire but the **PRE-2020 edge is economically zero** (Sharpe +0.22 / +0.31, mean ~+0.07 bp/day) — no standalone edge to insert, let alone after-cost PF≈2.0. Robust across the 3×3 n/thr grid (only barely-trading thr=1.5 dodges 2022, and even there no PRE-and-H1-positive cell). The only published standalone rates-MR result (jerryxyx curve-cointegration Sharpe 1.98) is a 2017 single-year **different** mechanism.
docs/rejected_candidates.md:255:**Rejection scope:** the direction (the ORB-MNQ-1 opening-range-breakout construct — 30-min OR from the 09:30 ET open, both-sides touch-fill, stop = opposite OR extreme, exit-at-close — transplanted to **ZB** as a *risk-off-decorrelated large-δ leg*) is rejected as an **entry** mechanism. Proposed to thread the Q-COMPOSE-1 / decompound-HOLD "vise" (a cost-viable breakout that is *counter-cyclical* to the index-momentum book); killed at the cheapest Phase-0 falsifier.
docs/rejected_candidates.md:260:**Surviving finding (NOT rejected) — load-bearing:** **opening-range momentum is an equity-index property; it does not transfer to Treasuries (ZB shows opening-range mean-reversion).** This *tightens the vise* — the one cost-viable mechanism class (large-δ index intraday breakout) is mechanistically tied to the equity-index book the locked/c1 legs already harvest, so cost-survival and decorrelation are in tension by construction, not merely empirically (Q-COMPOSE-1).
docs/rejected_candidates.md:264:<!-- concept-intake-entry mechanism_family="opening-range-breakout" instrument="ZB" rejection_reason="edge-failure (negative gross edge) + venue/cost-geometry: ORB-MNQ-1 opening-range-breakout construct (30-min OR from 09:30 ET, both-sides touch-fill, exit-at-close) transplanted to ZB (30Y T-bond) as a risk-off-decorrelated large-delta leg. K=0 delta-extraction on native ZB.v.0 (Databento GLBX, $0.00, 1m->15m ET, 2019-2026, n=1853), orb_lib.orb_backtest verbatim. Mean GROSS edge negative EVERY window (full -0.0480R t-1.61; 2021+ -0.0293; 2019 -0.0686; 2020 -0.1379) -> cost-law ratio -0.20x headline / -10.66x at 0-slip; net PF 0.59 WR 0.34. Within-day OR placebo p=0.0010 sign-reversed (real OR -0.265R LESS loss-making than arbitrary-window -0.545R -> ZB fades the opening range). Cost geometry hostile (median OR 10 ticks vs ~2-tick RT, cost_R 0.235R, 4x hurdle 0.94R) but moot under negative sign. Load-bearing: opening-range MOMENTUM is equity-index-specific; ZB shows opening-range MEAN-REVERSION." harness_disposition_ref="ORB-ZB-1 Phase-0 (K=0 delta-extraction, no harness DispositionRecord; lab/archive/orb_zb_recon_2026-07/RESULTS.md)" date="2026-07-20" class="edge-failure+venue-cost-geometry" role_tested="entry" falsifier_failed="P0.1 cost-law: negative gross edge every window (-0.20x headline, -10.66x 0-slip); within-day placebo p=0.0010 sign-reversed (breakouts lose every window; OR least-bad); net PF 0.59" addback_condition="NEW mechanism for a different ZB construct - NOT an anchor re-tune (09:30->08:30) or param sweep of this breakout; a ZB fade is a distinct mechanism with its own intake + adverse cost geometry" config_fingerprint="orb/ZB.v.0/OR2x15m@09:30ET/both/exit@close/rt=0.06372pt(Bulenox$0.61+1tick)/feed=databento-GLBX-ZB.v.0-1m(d2f56c0d)" -->
docs/rejected_candidates.md:265:- **opening-range-breakout on ZB** — rejected 2026-07-20 (edge-failure + venue/cost-geometry: ORB-MNQ construct transplanted to the 30Y T-bond as a risk-off-decorrelated large-δ leg; K=0 δ-extraction on native ZB.v.0 (Databento, $0.00, n=1,853) → **negative gross edge every window** (full −0.048 R, −0.20× headline / −10.66× at 0-slip), within-day placebo p=0.0010 sign-reversed → ZB *fades* its 09:30 opening range; opening-range momentum is equity-index-specific); `lab/archive/orb_zb_recon_2026-07/RESULTS.md`.
docs/rejected_candidates.md:282:**Rejection scope:** the direction (the ORB-MNQ-1/ORB-ZB-1 opening-range-breakout construct, OR-anchored at the 08:30 ET CPI/NFP release instead of the equity cash open, day-filtered to CPI+NFP announcement days only, on the CBOT 5-Year T-Note) is rejected as an **entry** mechanism — the one previously-untested cell in the program's rates-event 2×2 matrix (unconditional-drift × conditional-drift × unconditional-breakout × **conditional-breakout**), now closing the matrix fully dead.
docs/rejected_candidates.md:290:<!-- concept-intake-entry mechanism_family="conditional-event-anchored-orb" instrument="ZF" rejection_reason="edge-failure (marginal, cost-walled, underpowered) -- NOT venue/cost-geometry, NOT decorrelation-failure (both passed). ORB-MNQ/ORB-ZB construct OR-anchored at 08:30 ET CPI/NFP release, day-filtered to event days, on CBOT 5Y T-Note. K=0 delta-extraction (PRIMARY+SECONDARY K_intrinsic=2 pre-committed) on native ZF.v.0 (Databento, $0.00, n=143 of 179 CPI+NFP events, primary-BLS-sourced). P0.1 geometry PASS (17.62:1 vs ZB unconditional 4.3:1). P0.5 decorrelation PASS (rho=0.280, zero-padded). P0.2 PRIMARY cost-law KILL (mean gross +0.1033R t+1.45 n.s.; headline ratio 1.15x vs 4.0x bar; passes trivially at unrealistic 0-slip 15.94x). P0.4 power FAIL (0.3047 vs 0.50 bar). Placebo p=0.0010 informative not rescue (arbitrary-window breakouts strongly negative -0.39 on event days; OR window merely flat +0.014 -- least-bad not real edge). SECONDARY top-half-range subcohort no rescue (0.74x, net-negative). Per-year sign alternates (same noise signature as sibling NG-EIA-1 same day). Third of three distinct directional entry-construct shapes tested on genuine Treasury-complex instruments this session (ZN auction-drift H-ZNAUC-1; ZB unconditional-breakout ORB-ZB-1; ZF conditional-breakout, this closure) -- 0 survivors, 3 distinct failure modes; tail-methodology-exhaustion per INQHIORI §6 (not a formal domain-SNAG closure -- that bar in this file is calibrated to ~17-22 candidates, a different scale). CL-EIA/F-B is an adjacent informed-flow precedent on a DIFFERENT instrument (crude oil), not a fourth rates cell; a fixed-hold conditional-drift construct (no breakout/stop) was never itself run on a Treasury instrument." harness_disposition_ref="RATES-EV-ZF-1 Phase-0 (K=0 delta-extraction, no harness DispositionRecord; lab/archive/rates_ev_zf_recon_2026-07/RESULTS.md)" date="2026-07-21" class="edge-failure" role_tested="entry" falsifier_failed="P0.2 cost-law 1.15x vs 4.0x bar; P0.4 power 0.3047 vs 0.50 bar; per-year sign alternates (noise)" addback_condition="NEW mechanism evidence not a re-tune of event-set/OR-window/instrument within this conditional-breakout shape (closed at N=143/power=0.30); a 4th directional Treasury-complex construct at the same analysis level needs the parent question reformulated per INQHIORI §6, not just a new instrument/window" config_fingerprint="orb-event/ZF.v.0/OR2x15m@08:30ET-CPI+NFP/both/exit@15:00ET/rt=0.01685pt(Bulenox$0.61+1tick$7.8125)/feed=databento-GLBX-ZF.v.0-1m(3af3c763)/calendar=bls.gov-8yr-schedule-2019-2026(179events)" -->
docs/rejected_candidates.md:297:**Class:** edge-failure (the selection *dilutes* rather than concentrates edge — strictly dominated by the incumbent single-instrument ORB-MNQ) + data/universe-constraint (secondary — the 4–6-way ES/NQ/YM/RTY universe is unavailable without a real ES+RTY intraday pull).
docs/rejected_candidates.md:299:**Closure basis:** cheapest-falsifier necessary-condition pre-screen (Notice-phase, cached data, **no K bound**) on the widest-spread US large-cap pair we hold intraday — Nasdaq (`MNQ_M15`) vs Dow (`MYM_M15`), 1,534 common RTH sessions 2020-07→2026-07. **(A) DISPERSION** compressed-but-non-zero: `corr(RV_nq,RV_ym)=0.717`, 68% of days RV within ±25%. **(B) PREDICTIVENESS** fails on the metric that matters: the higher-RV index has a marginally bigger same-day \|move\| (+1.86 bp, sign-p 0.008) but **NOT** a better ORB edge (win 0.487, +0.22 bp, sign-p 0.329 — null, slightly wrong-signed). **Killer stat:** RV-rank selection captures **+2.64 bp** ORB edge vs +2.39 bp random and vs **+5.19 bp for always trading MNQ alone** (MYM ORB unconditional −0.35 bp) — the rotation gives *half* the incumbent single-instrument edge because ~half the days RV selects the weaker index (Dow). The Stocks-in-Play mechanism (in-play → better breakout) does not fire: in-play predicts a bigger but not more *directional* move (whipsaw, not edge).
docs/rejected_candidates.md:300:**Surviving finding (NOT rejected) — load-bearing:** the cross-index ranking is **strictly dominated by the incumbent single-instrument ORB-MNQ** — index aggregation compresses the idiosyncratic dispersion that makes Stocks-in-Play work (1,000-stock cross-section → 4–6 co-moving broad baskets), so a small-universe RV ranking harvests weak factor-rotation noise. This specializes the **venue-wall** pattern: the *strong* documented intraday edge (Stocks-in-Play, Sharpe 2.8) needs a **single-stock cross-section the futures-prop venue cannot host** — same class as crypto-trend (venue-walled) and dispersion/short-vol (options-free venue).
docs/rejected_candidates.md:303:<!-- concept-intake-entry mechanism_family="cross-index-relative-volume-ranking" instrument="ES-NQ-YM-index-futures" rejection_reason="edge-failure (selection dilutes not concentrates) + data/universe-constraint: recover the Zarattini Stocks-in-Play cross-sectional ORB selection edge by ranking US equity-index futures (ES/NQ/YM/RTY) on opening relative volume, trading ORB only on the most in-play index/day. Cheapest necessary-condition pre-screen (Notice-phase, cached data, no K) on the 2 indices held intraday = Nasdaq MNQ_M15 vs Dow MYM_M15 (widest US large-cap spread), 1534 common RTH sessions 2020-07..2026-07. (A) DISPERSION corr(RV)=0.717, 68% days RV within +/-25% (compressed non-zero). (B) PREDICTIVENESS: higher-RV bigger |move| +1.86bp sign-p0.008 but NOT better ORB edge (win 0.487 / +0.22bp / sign-p0.329, null slightly wrong-signed). Killer: RV-selection ORB edge +2.64bp vs random +2.39bp vs always-MNQ +5.19bp (MYM uncond -0.35bp) -> rotation captures HALF the incumbent single-instrument edge. In-play predicts bigger but not more directional move (whipsaw). Strictly dominated by ORB-MNQ. 4-6-way ES/NQ/YM/RTY universe unavailable without a real ES+RTY intraday pull (only daily ES cached; no RTY)." harness_disposition_ref="cross-index RV necessary-condition pre-screen (Notice-phase, no harness DispositionRecord; lab/archive/xindex_rv_recon_2026-07/RESULTS.md)" date="2026-07-21" class="edge-failure+data-universe-constraint" role_tested="selection-gate" falsifier_failed="(B) higher-RV NOT better ORB edge (win 0.487, +0.22bp, sign-p0.329); RV-selection +2.64bp < always-MNQ +5.19bp (dominated by incumbent); (A) dispersion compressed corr(RV)=0.717" addback_condition="scoped ES+RTY intraday pull showing small-cap idiosyncrasy raises RV dispersion AND higher-RV then predicts better ORB edge (DEFER-procurement, poor prior) - NOT an RV-window/ORB/2-index re-tune; ES-alone inadmissible (more homogeneous)" config_fingerprint="xindex-rv/MNQ_M15+MYM_M15/open30m-RV-lookback14/ORB-first-break-exit-close/n=1534/2020-07..2026-07/feed=core-data-bar_data" -->
docs/rejected_candidates.md:304:- **cross-index-relative-volume-ranking on ES/NQ/YM index futures** — rejected 2026-07-21 (edge-failure + data-universe-constraint: recover the Stocks-in-Play cross-sectional ORB selection edge by ranking index futures on opening relative volume; cheapest necessary-condition pre-screen on the 2 indices held intraday (Nasdaq MNQ vs Dow MYM, n=1,534) → dispersion compressed (corr 0.717) and higher-RV does NOT predict a better ORB edge (win 0.487, sign-p 0.329); RV-selection captures +2.64 bp vs **+5.19 bp for always-MNQ** → strictly dominated by the incumbent single-instrument ORB-MNQ; the strong Stocks-in-Play edge needs a single-stock cross-section the futures-prop venue can't host); `lab/archive/xindex_rv_recon_2026-07/RESULTS.md`.
docs/rejected_candidates.md:342:### Third-Friday derivative-settlement reversal on MYM
docs/rejected_candidates.md:344:**Rejection scope:** the exact Baltussen/Terstegge/Whelan derivative-payoff-bias expression on native MYM: short the calendar third-Friday 09:30 ET open and cover at 12:00 ET. The overnight Thursday-close→Friday-open spike is a mechanism-faithfulness measurement, not a traded limb.
docs/rejected_candidates.md:347:**Authoritative artifact:** [`lab/archive/mym_3fps_recon_2026-07/RESULTS.md`](lab/analysis/lab/archive/mym_3fps_recon_2026-07/RESULTS.md) + [`closure`](briefs/closures/MYM-3FPS-1-closure-falsified.md).
docs/rejected_candidates.md:348:**Closure basis:** frozen K=0 native-micro extraction, 2019-05-06→2026-07-21, exact timestamps and no nearest-bar substitutions. Coverage passed (84/87, 96.6%), but the overnight spike was only +1.54 bp (`delta/sigma=0.0256`, power 0.042) and the open-to-noon short only +2.68 bp (`delta/sigma=0.0500`, power 0.067), both far below the frozen 0.2139 standardized-effect floor. The short also failed the Tradeify cost law: +2.68 bp vs 6.57 bp 4× hurdle. Year signs were unstable and the tradable limb was negative in 2019, 2024, 2025, and 2026. The published ~12 bp DJIA effect does not transfer at useful magnitude to the native MYM era.
docs/rejected_candidates.md:349:**Re-proposal bar:** new target-instrument mechanism evidence. NOT a 09:15/09:20 entry, different exit, quarterly/triple-witch subset, MNQ rescue, overnight limb, or pooled-index version; each is a new hypothesis and the first three are precisely the post-result selection moves this probe froze out.
docs/rejected_candidates.md:351:<!-- concept-intake-entry mechanism_family="third-friday-derivative-settlement-reversal" instrument="MYM" rejection_reason="edge-failure + venue/cost-geometry: frozen K=0 native-MYM third-Friday 09:30->12:00 short, n=84/87 exact events (96.6%). Overnight spike +1.54bp, delta/sigma 0.0256, power 0.042; open-to-noon short +2.68bp, delta/sigma 0.0500, power 0.067; both below 0.2139 floor. Cost-law FAIL: +2.68bp vs 6.57bp 4x Tradeify hurdle. Year signs unstable; short negative 2019/2024/2025/2026. Published ~12bp DJIA effect absent at useful magnitude in native MYM era." harness_disposition_ref="MYM-3FPS-1 Phase-0 (K=0 delta extraction; lab/archive/mym_3fps_recon_2026-07/RESULTS.md)" date="2026-07-21" class="edge-failure+venue-cost-geometry" role_tested="entry" falsifier_failed="P0.1 overnight delta/sigma 0.0256; P0.2 reversal delta/sigma 0.0500 vs 0.2139 floor; P0.3 +2.68bp vs 6.57bp hurdle" addback_condition="new target-instrument mechanism evidence - NOT timing/exit/expiry-subtype retune, MNQ rescue, overnight limb, or pooled-index variant" config_fingerprint="3fps/MYM.v.0/calendar-third-Friday/short-open09:30ET->12:00ET/cost=Tradeify0.91+1tick-side/feed=Databento-GLBX-MYM.v.0-ohlcv1m-2019-05-06..2026-07-21" -->
docs/rejected_candidates.md:352:- **third-Friday-derivative-settlement-reversal on MYM** — rejected 2026-07-21 (edge-failure + cost: native K=0 exact-window probe, n=84; overnight +1.54 bp / power 0.042; short reversal +2.68 bp / power 0.067; cost hurdle 6.57 bp; unstable and recently wrong-signed); `lab/archive/mym_3fps_recon_2026-07/RESULTS.md`.
docs/rejected_candidates.md:354:### Opening-volume × directional-efficiency pressure map on MNQ/MYM
docs/rejected_candidates.md:356:**Rejection scope:** the continuous BAR EXPORT opening-pressure mechanism — high opening volume as continuation when the first 30 minutes are directionally efficient and as reversal when absorbed into a low-efficiency range — on native MNQ and MYM M15 panels. Not a strategy or entry rule.
docs/rejected_candidates.md:360:**Closure basis:** frozen K=0 hash-pinned diagnostic (`MNQ_M15.csv` `ddb14f…e1f7e3ac`, `MYM_M15.csv` `298ab8…f9059c`). Neither instrument passed. MNQ development t=1.53 and pooled t=1.60 (both <2) despite positive slopes and a cost-clearing P90−P10 spread; MYM development slope wrong-signed (−3.63 bp) and predicted spread 1.71 bp below the 6.41 bp 4× Tradeify hurdle. Exactly-zero instruments passed → overall `FALSIFIED` (not AMBIGUOUS).
docs/rejected_candidates.md:363:<!-- concept-intake-entry mechanism_family="opening-volume-directional-efficiency" instrument="MNQ+MYM" rejection_reason="edge-failure: frozen K=0 BAR EXPORT pressure-alignment diagnostic. MNQ FAIL (dev t=1.53, pooled t=1.60 <2); MYM FAIL (dev slope -3.63bp wrong-signed; pred spread 1.71bp < 6.41bp 4x cost). Neither PASS → FALSIFIED." harness_disposition_ref="OPENPRESS-1 (lab/archive/opening_pressure_map_2026-07/RESULTS.md)" date="2026-07-21" class="edge-failure" role_tested="mechanism-diagnostic" falsifier_failed="MNQ HAC t<2; MYM wrong-signed + cost FAIL" addback_condition="new modality/mechanism - NOT threshold/window/instrument rescue on same OHLCV" -->
docs/rejected_candidates.md:364:- **opening-volume × directional-efficiency on MNQ/MYM** — rejected 2026-07-21 (edge-failure: frozen continuous pressure score; MNQ underpowered HAC t; MYM wrong-signed + cost FAIL; neither PASS); `lab/archive/opening_pressure_map_2026-07/RESULTS.md`.
docs/rejected_candidates.md:378:### Closing-auction / MOC-imbalance flow on MYM — paid-data 5th-leg candidate
docs/rejected_candidates.md:381:16:00 ET close) as a directional entry on MYM, flat well before the 16:45 ET deadline. Rejected as a
docs/rejected_candidates.md:389:**Authoritative artifact:** [`docs/briefs/2026-07-27-f1-moc-imbalance-mym-ruling.md`](briefs/2026-07-27-f1-moc-imbalance-mym-ruling.md)
docs/rejected_candidates.md:397:**UNSCREENABLE** (no MOC→MYM δ; transplant and invention both forbidden), and the δ-extraction probe
docs/rejected_candidates.md:400:pure arithmetic): MYM RT $2.82 ⇒ 4× hurdle $11.28 ⇒ ≈22.6 Dow points/trade in a ten-minute window.
docs/rejected_candidates.md:407:<!-- concept-intake-entry mechanism_family="closing-auction-moc-imbalance-flow" instrument="MYM" rejection_reason="paid-data-procurement-gate (reject-at-bar): census entry F1 - trade published MOC order imbalance (15:50 ET publication -> 16:00 ET close) directionally on MYM, flat by 16:45. Clears NO route: free-data route 1 requires demonstrating a vol-orthogonal + within-era-robust edge and F1 has zero delta/cohort/measurement (unclaimed, not cleared); no new venue class; no dated incident. Binding constraint = the standing 'don't buy explanatory data before a survivor justifies it' rule, operationalised by the 2026-07-24 Avenue-A scoping (qualifying triple unmet, scoped-not-procured) - F1 is blind discovery on paid data with no survivor tie. Independently UNSCREENABLE under harvest Req 2 (no MOC->MYM delta; transplant/invention forbidden; delta-extraction probe circular since it needs the gated data). Unvalidated cash-equity -> micro-Dow-future transmission. NOT killed by the D2 free-data classification (imbalance is exchange-licensed, not public-derivable) nor by the a4 category prior (published signed imbalance != category splitting) - those distinctions are stated so a future session does not borrow the wrong kill." harness_disposition_ref="F1-bar-ruling (manual paid-data-procurement-gate falsifier; docs/briefs/2026-07-27-f1-moc-imbalance-mym-ruling.md)" date="2026-07-27" class="paid-data-procurement-gate" role_tested="entry" falsifier_failed="no route cleared: free-data route 1 unclaimed (zero demonstration), OHLCV route-2 order-flow modality gated by no-buy-before-survivor + Avenue-A qualifying triple, harvest Req 2 UNSCREENABLE with circular probe route" addback_condition="published cohort delta for imbalance->index-futures response citable WITHOUT procurement (free, zero-K, only route attemptable today), OR a survivor tie meeting Avenue-A section-6 qualifying triple, OR the data becoming free (which drops it into the D2 free-data kill), OR a dated live incident - NOT micro-capacity re-framing, different index, longer window, or a well-formed four-clause card" config_fingerprint="moc-imbalance/MYM/signal=exchange-published-signed-imbalance/window=1550-1600ET/venue=futures-prop-flat-1645" -->
docs/rejected_candidates.md:408:- **closing-auction-moc-imbalance-flow on MYM** — rejected 2026-07-27 (paid-data-procurement-gate: no route cleared; free-data route 1 unclaimed for want of any δ; order-flow modality gated by "don't buy explanatory data before a survivor" + Avenue-A qualifying triple; UNSCREENABLE under Req 2 with a circular probe route); [`docs/briefs/2026-07-27-f1-moc-imbalance-mym-ruling.md`](briefs/2026-07-27-f1-moc-imbalance-mym-ruling.md).
docs/rejected_candidates.md:410:### ORB-MNQ-1 as a payable standalone `Tradeify_Select_100K` leg — DEPLOYMENT-TARGET rejection (NOT a mechanism rejection)
docs/rejected_candidates.md:413:firm**, not the ORB mechanism family and not ORB on MNQ. It is filed here so the re-proposal bar is
docs/rejected_candidates.md:416:instrument="MNQ"` return REJECTED to every future caller, which is not what was decided.
docs/rejected_candidates.md:418:**Rejection scope:** the *target* — running the frozen ORB-MNQ-1 construct at k ∈ {1,2,3} as a
docs/rejected_candidates.md:427:**Authoritative artifact:** [`docs/adr/2026-08-03-orb-mnq-repark-payability-falsified.md`](adr/2026-08-03-orb-mnq-repark-payability-falsified.md)
docs/rejected_candidates.md:429:[`RESULTS_t2_intraday_bust.md`](lab/analysis/lab/analysis/orb/orb_mnq_2026-07/RESULTS_t2_intraday_bust.md),
docs/rejected_candidates.md:460:domain. Precedent: the Guardian-on-XAGUSD entry closed on parent-programme
docs/rejected_candidates.md:533:**Basis (why a raised bar, not a closure):** 4 own in-domain closures — **D5** (Stage-2 cost-law, 2026-07-16) / **D5-RECOST** (OOS edge decayed negative, 2026-07-21) / **H-TSMOM-1** (Clause-N power, 2026-07-16) / **cross-index-RV-ranking** (dominated by incumbent, 2026-07-21) — **plus 1 admitted survivor `ORB-MNQ-1` (lifecycle CANDIDATE @1.00×, 2026-07-16)** + external corroboration (two 2026-07-21 literature deep-searches; independent MNQ 0/14-family falsification, arXiv 2605.04004). The count is ~⅓ of this file's ~17–22 domain-SNAG bar and the domain is **1-admission, not 0**, so the audit declined SNAG per the same-week **ZF calibration** (3 constructs = INQHIORI §6 tail-exhaustion, not SNAG). The three cost/edge-ratio levers are now mapped — **price** (D5-RECOST: moot, edge decayed), **instrument-selection** (cross-index: dilutes below the single best incumbent), **hold-time** (ORB-MNQ already exploits it via exit-at-close) — so a re-tune of any lever is the exhausted move.
docs/rejected_candidates.md:539:   > closure below, which measured *dilution across a universe* (+2.64 bp RV-ranked vs **+5.19 bp always-MNQ**) —
docs/rejected_candidates.md:552:3. evidence it **beats the incumbent ORB-MNQ net-of-cost**, not merely clears the cost floor.
docs/rejected_candidates.md:553:**Explicitly preserved (NOT rejected):** `ORB-MNQ-1` (the survivor) and the **session-confluence longer-hold** thread (untested, low-priority — ORB-MNQ already occupies that class). Reviewed at the 2026-08-08 slate; escalates to a genuine domain-SNAG only if own in-domain closures reach ~17–22 **and** ORB-MNQ is retired to 0 (audit §10 hook 3).
docs/rejected_candidates.md:554:**⚠ Status update 2026-08-02 — the session-confluence longer-hold preservation is DISCHARGED, not still untested.** `Q-SESSCONF-1` measured it and closed **FALSIFIED** ($0/K=0): the hold-window ceiling is **+0.091 annSR** against a **+0.124** K-price, and the externally-carved-out **60–75 min class measures +0.501/+0.490 against the incumbent's +0.842** — adverse, not merely unproven. [`lab/analysis/orb/sessconf_mnq_2026-08/RESULTS.md`](lab/analysis/lab/analysis/orb/sessconf_mnq_2026-08/RESULTS.md). The survivor preservation is unchanged.
docs/rejected_candidates.md:568:**not** cover: the incumbent `ORB-MNQ-1`; the *exit-time* question itself (settled separately by
docs/rejected_candidates.md:569:[`ADR 2026-07-31`](adr/2026-07-31-orb-mnq-unpark-payability-target.md) §5, which bars adopting the
docs/rejected_candidates.md:578:| 3 | Drift exhaustion against a constant hazard | **FALSIFIED** | OOS on MYM: L1/L2 passed but `t*` degenerate at **03:15 ET** (before the session opens); P3 missed by **16×** tolerance |
docs/rejected_candidates.md:582:index futures for the first time, with per-day standard errors: MNQ final block **t = −1.78**, and
```

### instrument_profiles cell consult — all 7 symbols

Command (verbatim; `;` continued on non-zero):

```
python scripts/instrument_profiles.py cell MYM placeholder
python scripts/instrument_profiles.py cell MNQ placeholder
python scripts/instrument_profiles.py cell MES placeholder
python scripts/instrument_profiles.py cell MGC placeholder
python scripts/instrument_profiles.py cell M2K placeholder
python scripts/instrument_profiles.py cell MCL placeholder
python scripts/instrument_profiles.py cell M6A placeholder
```

Full stdout + exit codes:

```
===== cell MYM placeholder =====
FATAL: unknown mechanism 'placeholder'. Declare it NEW in MECHANISMS.md.

EXIT=2

===== cell MNQ placeholder =====
FATAL: unknown mechanism 'placeholder'. Declare it NEW in MECHANISMS.md.

EXIT=2

===== cell MES placeholder =====
FATAL: unknown mechanism 'placeholder'. Declare it NEW in MECHANISMS.md.

EXIT=2

===== cell MGC placeholder =====
FATAL: unknown mechanism 'placeholder'. Declare it NEW in MECHANISMS.md.

EXIT=2

===== cell M2K placeholder =====
FATAL: unknown mechanism 'placeholder'. Declare it NEW in MECHANISMS.md.

EXIT=2

===== cell MCL placeholder =====
FATAL: unknown mechanism 'placeholder'. Declare it NEW in MECHANISMS.md.

EXIT=2

===== cell M6A placeholder =====
FATAL: unknown mechanism 'placeholder'. Declare it NEW in MECHANISMS.md.

EXIT=2
```

**ENV-1 housekeeping (design §11 / M6A):** CLOSED for missing ledger, still FATAL on mechanism id. `ops/instruments/M6A.md` exists (created 2026-08-11; `profiles.json` lists M6A among 26 ledgers). Consult order is ledger-then-mechanism, so M6A did **not** print `FATAL: no ledger`. All 7 symbols exit **2** with `FATAL: unknown mechanism 'placeholder'. Declare it NEW in MECHANISMS.md.` — `placeholder` is not in `MECHANISMS.md`. The missing-ledger FATAL an older brief expected is stale; do not treat this as a silent skip.

**Execute-time amendment (post-compile, PREREG F7 clause):** the rg paste above is the Block-1 compile snapshot (`b8` heading then PARK/PROPOSED). After merge of `origin/main` (PR #751 / SESSIONS `11z`), [`b8`](lab/archive/../../../docs/pursuits/b8-guardian-mgc-transfer-lane.md) Standing is **SUBTRACT** and the cell is closed [`DEAD(N-SURV)`](lab/archive/../../../docs/briefs/closures/2026-08-11-guardian-mgc-transfer-cell-dead-nsurv.md). Compile DEDUP keeps `guardian×MGC` as `PARKED(b8)` (F7 freeze; closure says Q-TXG-1 compile untouched). Cell remains non-OPEN. H_A unchanged.

## §6 What this does NOT establish
1. No OPEN cell is a candidate — Phase B needs operator election + cell PREREG + native-TV panel.
2. S7 bindingness with withdrawn legs is undisclosed-as-kill — Block 2 re-reads the third-leg spec.
3. W-COST measured_edge_R table is empty (no PnL-derived constants); residual kill awaits Phase-B panel.
4. ATR(14)/ATR(19) stop mapping is UNSCREENABLE for Guardian/Aegis — not an invitation to invent ATR.
5. Compile DEDUP keeps Guardian×MGC `PARKED(b8)` (PREREG F7). Pursuit standing after `11z` is SUBTRACT / `DEAD(N-SURV)` — not a Block-1 election; re-entry is new-mechanism armor, not a locked-parameter retune.
6. Harvest Req 1–5, DSR-at-K, N-SURV, regime gate are unweakened.

## §7 Reproduce
python -X utf8 lab/archive/transfer_expression_grid_2026-08/run_grid_compile.py --self-check
python -X utf8 lab/archive/transfer_expression_grid_2026-08/run_grid_compile.py --compile
python -X utf8 -m pytest lab/archive/transfer_expression_grid_2026-08/test_grid.py -v
