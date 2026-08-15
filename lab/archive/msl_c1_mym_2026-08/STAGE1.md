# MSL-C1 Stage-1 — MYM PDH/PDL failed-break reclaim (pre-G0)

**Status:** `STAGE-1 PASS` · **B4 GO 2026-08-13** → [`PREREG_G0.md`](PREREG_G0.md) **FROZEN** · explore **FALSIFIED** ([`RESULTS_g2.md`](RESULTS_g2.md) · [closure](lab/archive/../../docs/briefs/closures/MSL-C1-closure-falsified.md)) · Pine not authorized · **$0 · K=0**
**Card:** MSL-C1 · instrument **MYM** · mechanism **`pdh-pdl-failed-break-reclaim`** (existing class; C3 minted NEW on M2K then OPERATOR-KILL — class stands)
**Parent:** [MSL charter](lab/archive/../../docs/spec/2026-08-12-msl-manual-sourcing-loop-charter.md) steps 2–4 · [slate §MSL-C1](lab/archive/../../docs/briefs/2026-08-12-msl-first-slate.md) · [B8 occupancy](lab/archive/../../docs/adr/2026-08-12-msl-mym-occupancy-release.md) · [implied-SR report-only](lab/archive/../../docs/adr/2026-08-13-implied-sr-report-only-fade-reopen.md)
**Evidence CLI:** [`card.yaml`](card.yaml) · [`preflight.json`](preflight.json) (`msl_preflight` — evidence only)
**Handoff:** C3 [OPERATOR-KILL](lab/archive/../../docs/briefs/closures/MSL-C3-closure-operator-kill.md) → this card

---

## Freeze (zero data contact)

| Field | Frozen value |
|---|---|
| Reference class | **Prior-day RTH high/low (PDH/PDL)** — only level class licensed |
| Direction | Fade **failed** break (reclaim after non-follow-through) |
| Timing | 15m reclaim confirmation |
| Stop / exit | Structural beyond swept extreme; truncated-loss exit management; flat by 16:00 ET |
| Cadence | k=1; first valid signal per session |
| Not licensed | Overnight extreme; OR boundary; through-break; additional level class (+1 K_intrinsic each) |

**Route (ONE):** **①** — SLR MR-at-level precedent ([SLR-MYM-1 closure](lab/archive/../../docs/briefs/closures/SLR-MYM-1-closure-falsified-stage0.md) gate 0-B CLEAR). Cite; do not re-argue.

**CONFIRM window (named before any read; unread through step 8):** `2025-09-01 → 2026-08-13`.
**IS:** everything before `2025-09-01`. This Stage-1 pass did **not** read either partition.

**Rejected nearest classes:**
- `pdh-pdl-breakout-rth` — through-break (CON-4); opposite selector
- `ict-liquidity` — SLR-MYM-1 DEAD cell; ICT weekly-gated first-30m sweep — different framing; Stage-0 FALSIFIED as scoped (mechanism never tested)
- `opening-range-continuation` / `opening-pressure` — DEAD on MYM
- `mean-reversion-fade` — USOIL spike-fader entry bar; role-asymmetry does not auto-clear entry here — C1 rests on route ① + delete/flip alone
- C3 M2K unpaid path — OPERATOR-KILL; **not** a class kill; this is a different instrument election

---

## Cost basis (Rule 0)

Tradeify Select 100K Equity Index: `$0.91`/side · tick `$0.50` · MYM **$0.50/pt**:

`RT = 2×$0.91 + 2×$0.50 = $2.82` · 4× = **$11.28**/contract/trade.

**Design point:** n=1 entry/day · 4 contracts · stop **320.0 pts** ($160 R/ct) · target 320.0 pts (rr=1 for tables only). **`p` / `rr` are not freeze-time claims.**

---

## Step 2 — Dedup + door-check (executed)

### Cell consult (raw)

`cell_returncode=1` is expected whenever a BINDING BAR is present (`instrument_profiles.cmd_cell`);
preflight still exits 0 (evidence only). Cleared in the door-check table below via route ① + B8.

```
$ python scripts/instrument_profiles.py cell MYM pdh-pdl-failed-break-reclaim
=== MYM x pdh-pdl-failed-break-reclaim ===
ledger: ops/instruments/MYM.md
venue: NOT TRADABLE at the live firm — AUTHORIZED-but-venue-less incumbent (Striker DJ30 MYM edition); no live book to correlate new work against — check venue_note before book-correlation gate.
verdict: untested — no prior on this cell.
class finding (mechanism-wide, not specific to MYM): none yet — M2K Stage-1 PASS then [OPERATOR-KILL](lab/archive/../docs/briefs/closures/MSL-C3-closure-operator-kill.md) (B4 declined; class not killed); MYM Stage-1 PASS (C1), B4 unpaid. [C3 STAGE1](lab/archive/../lab/analysis/c1/msl_c3_m2k_2026-08/STAGE1.md) · [C1 STAGE1](lab/archive/../lab/archive/msl_c1_mym_2026-08/STAGE1.md)
BINDING BAR: index-intraday-ohlcv-directional-timing-2026-07-21 -> ../../docs/rejected_candidates.md
cost hurdle: 6.57 bp/event (4x Tradeify hurdle) — VERIFY at #M6
K bank: read ../../discovery_manifests/ — never trust a snapshot.
prior: Not a barren instrument — the incumbent locked leg is profitable here; one narrow continuation expression failed. [#M1]
```

(Full stdout pinned in [`preflight.json`](preflight.json).)

### BINDING BAR / domain answers

| Bar / domain item | Route answer |
|---|---|
| `index-intraday-ohlcv-directional-timing-2026-07-21` | **CLEAR via route ①** — SLR MR-at-level clearance (cite; do not re-argue). |
| Occupancy / S3 | **CLEAR via B8** — [`ADR 2026-08-12`](lab/archive/../../docs/adr/2026-08-12-msl-mym-occupancy-release.md): `MYM1!` released for new non-Striker MSL research/G0. S1 keep-warm + Striker redeploy bar stand. PROFILE `venue_tradable: false` is Striker-withdrawn posture, not an MSL research ban. |
| Dense-1m “forbids PDH/PDL θ” | **Lane-scoped — does not bind.** [`dense1m lane`](lab/archive/../../docs/spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md) forbids a *new CON family* that duplicates CON-4 PDH/PDL **through-break** on dense-1m. This card is session-scale **15m failed-break reclaim** (opposite selector) outside that lane. |
| Q-TXG-1 lane bar | **Does not bind** — new mechanism (non-transfer); C1 is not a transfer cell. |
| SLR-MYM-1 | Adjacent — framings failed delete/flip; **Req 1a still mandatory** on IS before Pine. Not a free pass. |

### Dedup needles (paste summary)

```
docs/briefs/2026-08-12-msl-first-slate.md — MSL-C1 card
docs/briefs/closures/SLR-MYM-1-closure-falsified-stage0.md — Stage-0 FALSIFIED; route 1 CLEAR
docs/briefs/closures/MSL-C3-closure-operator-kill.md — same mechanism × M2K unpaid path killed
docs/adr/2026-08-12-msl-mym-occupancy-release.md — B8
ops/instruments/MYM.md — ORC DEAD; ict-liquidity DEAD (SLR); B8 session log
docs/rejected_candidates.md — RAISED BAR; OR continuation
```

---

## Step 3 — $0 screens at RT $2.82 (three kill limbs)

| Limb | Number | Gate | Verdict |
|---|---|---|---|
| cost-law | R/ct = **$160** vs 4×RT **$11.28** (tax 0.0176R); 320 pts ≫ 40-tick wide-stop floor | gross/trade ≥ $11.28 | **PASS** |
| payability | all-win day = **$628.72** | ≥ $200 | **PASS** |
| survival | all-lose day = **$651.28** | ≤ $750 | **PASS** |

Disclosures (non-gating): σ_d ≈ $636.79 vs $3,000 trail · implied-SR ≈ **1.60** under placeholder p=0.55 (not a kill — [`ADR 2026-08-13`](lab/archive/../../docs/adr/2026-08-13-implied-sr-report-only-fade-reopen.md)).

**Entry-rate honesty (N-ACT):** designed 1 entry/session ≈ 252/yr — above ~1/week solo floor. Measured failure-rate unpaid until G0 panel / TV (W4 / export).

---

## Step 4 — Cheap falsifier

1. **Cost-law at frozen geometry** — PASS ($160 ≫ $11.28).
2. **Occupancy + lane scope** — B8 CLEAR; dense-1m PDH/PDL bar lane-scoped — PASS.
3. **Delete/flip (Req 1a)** — unpaid at Stage-1 arithmetic; **mandatory before Pine/TV** (IS-only). Sham: replace PDH/PDL with a non-prior-day clock level; FLIP: join the extension at the reclaim bar.

---

## Verdict

**STAGE-1 PASS**. **B4 GO paid** → G0 frozen → explore **FALSIFIED** ([`RESULTS_g2.md`](RESULTS_g2.md)). No Pine. No K spend. CONFIRM unread.

**Next:** STOP this card — [closure](lab/archive/../../docs/briefs/closures/MSL-C1-closure-falsified.md).

---

## Iterate

- **Next:** STOP.
- **Board write:** plan §6 P3.3 → FALSIFIED (explore IS); first slate exhausted.
