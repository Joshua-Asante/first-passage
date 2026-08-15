# MSL-C2 Stage-1 — MGC London-range failed-extension fade (pre-G0)

**Status:** `STAGE-1 PASS` · **B4 GO paid 2026-08-12** · G0 [`PREREG_G0.md`](PREREG_G0.md) **FROZEN** · explore **ISSUED → FALSIFIED 2026-08-13** ([`RESULTS_g2.md`](RESULTS_g2.md)) · Pine not authorized · **$0 · K=0**
**Card:** MSL-C2 · instrument **MGC** · mechanism **`london-range-failed-extension-fade`** (NEW)
**Parent:** [MSL charter](lab/archive/../../docs/spec/2026-08-12-msl-manual-sourcing-loop-charter.md) steps 2–5 · [slate](lab/archive/../../docs/briefs/2026-08-12-msl-first-slate.md) · [implied-SR report-only ADR](lab/archive/../../docs/adr/2026-08-13-implied-sr-report-only-fade-reopen.md)
**Evidence CLI:** [`card.yaml`](card.yaml) · [`preflight.json`](preflight.json) (`msl_preflight` — evidence only)
---

## Freeze (zero data contact)

| Field | Frozen value |
|---|---|
| Reference class | London session high/low formed before COMEX RTH |
| Direction | Fade **failed** extension into COMEX open (reclaim after non-follow-through) |
| Stop / exit | Structural beyond swept London extreme; truncated-loss; flat by 16:00 ET |
| Cadence | k=1; first valid signal per session |
| Not chosen | Asia-range; join-on-confirmation; any fix/auction window |

**CONFIRM window (named before any read; unread through step 8):** `2025-09-01 → 2026-08-12`.
**IS:** everything before `2025-09-01`. This Stage-1 pass did **not** read either partition.

**Rejected nearest classes** (also in `MECHANISMS.md`):
- `event-window-reversal` — R8/LBMA-fix; not session-structure displacement
- `venue-transfer` / `trend-following` — Guardian→MGC DEAD(N-SURV); not a port
- `pdh-pdl-breakout-rth` / `opening-range-continuation` — through-break; opposite direction
- `mean-reversion-fade` — generic MR (USOIL spike-fader); London-range *failure* is the selector

---

## Cost basis (Rule 0)

Tradeify Select 100K Metals: `firm_rules.py` comment pin **MGC=$1.06**/side · tick_value **$1.00** · 1 tick/side slip (fade-spec convention):

`RT = 2×$1.06 + 2×$1.00 = $4.12` · 4× hurdle = **$16.48**/contract/trade.

Not used: envelope $2.90 · `cost_mgc.py` $3.24 · fixture $2.12.

**Design point:** n=1 entry/day · 4 contracts · stop **160 ticks / 16.0 pts** ($160 R/ct) · target 16.0 pts (rr=1 for geometry tables only). **`p` / `rr` are not freeze-time claims.**

---

## Step 2 — Dedup + door-check (executed)

### Cell consult (raw)

```
$ python scripts/instrument_profiles.py cell MGC london-range-failed-extension-fade
=== MGC x london-range-failed-extension-fade ===
ledger: ops/instruments/MGC.md
verdict: untested — no prior on this cell.
BINDING BAR: free-data-5th-leg-snag-closed-2026-07-01 -> ../../docs/rejected_candidates.md
K bank: read ../../discovery_manifests/ — never trust a snapshot.
prior: Third-leg E-K elimination is void as a gate after K-bank ADR; …
```

### BINDING BAR answers

| Bar / domain item | Route answer |
|---|---|
| `free-data-5th-leg-snag-closed-2026-07-01` | **CLEAR by domain mismatch** under ratified **R-FRAMING = §2.1**: Tradeify-native survival construct sits outside free-data 5th-leg SNAG scope (within-strategy alpha / free-exogenous regime gates / published-retail / chop-native decorrelated legs). C2 is not a 5th-leg expansion candidate. Not walking the three re-proposal routes. |
| Index intraday OHLCV raised bar | **Does not bind** — MGC is not an equity-index future (Stage-0 omitted it on purpose). |
| R-FRAMING status | **§2.1 governs** (Board B1); recorded here as the card line. |

### Dedup `rg` (mechanism family + role) — paste

Needle set: London-range / session-displacement / MGC / gold-fix / Guardian-transfer / SNAG / event-window.

```
docs/adr/2026-08-12-msl-sourcing-channel-ratification.md:25: … R-FRAMING … §2.1 … outside the free-data 5th-leg SNAG domain …
docs/briefs/2026-08-12-msl-first-slate.md:22–28: MSL-C2 card (this campaign)
lab/CATALOG.md:116: tnec_l2_sourcing_2026-08-10 … R8 gold-fix δ-extracted SCREEN-FAIL …
docs/rejected_candidates.md:27,71–85: Guardian→MGC transfer cell DEAD(N-SURV) …
docs/rejected_candidates.md:443–452: LETF EOD free-data 5th-leg (index; not MGC)
docs/rejected_candidates.md:541+: 5th-leg / portfolio-expansion SNAG-CLOSED 2026-07-01
docs/rejected_candidates.md:389: R8 gold benchmark-fix family scope cited adjacent to MCL TAS
ops/instruments/MGC.md: bars: free-data-5th-leg-snag-closed-2026-07-01 (Stage-0 #770)
ops/instruments/MGC.md DEAD: event-window-reversal / R8 SCREEN-FAIL (family-scoped)
```

`msl_preflight` needle `london-range-failed-extension` → **0 hits** (no prior of this construct).

### Adjacencies (not bars)

- **R8** metals-fix / `event-window-reversal` SCREEN-FAIL — family DEAD on MGC. C2 is not a fix-window idea; do not borrow R8 δ or re-proposal bar.
- **Guardian→MGC** `DEAD(N-SURV)` 42.2/72.4/16.5 — transfer barred; loss-side anti-pattern. New mechanism only.

---

## Step 3 — $0 screens at RT $4.12 (three kill limbs)

Campaign-manager adjudication (not the CLI):

| Limb | Number | Gate | Verdict |
|---|---|---|---|
| cost-law | R/ct = **$160** vs 4×RT **$16.48** (tax 4.12/160 = 0.026R) | gross/trade ≥ $16.48 | **PASS** |
| payability | all-win day = **$623.52** | ≥ $200 | **PASS** |
| survival | all-lose day = **$656.48** | ≤ $750 | **PASS** |

Disclosures (non-gating): σ_d ≈ $637 vs $3,000 trail · implied-SR ≈ **1.60** under placeholder p=0.55 (evidence only; not a kill — [`ADR 2026-08-13`](lab/archive/../../docs/adr/2026-08-13-implied-sr-report-only-fade-reopen.md)) · envelope $2.90 is **not** the screen basis.

**Clause-N frequency honesty:** designed 1 entry/session ≈ 252 events/yr — not D3/D7 monthly-dead. No δ/σ invented from gold prices; unpaid as a measured power limb until a G0 panel exists.

---

## Step 4 — Cheap falsifier

1. **Cost-law at frozen geometry** — PASS ($160 ≫ $16.48). Did not invent `p` to rescue.
2. **Adjacency scope** — freeze is neither R8 nor Guardian-transfer — PASS.
3. **Delete/flip (Req 1a)** — unpaid at Stage-1 arithmetic; **mandatory before Pine/TV** — declared in [`PREREG_G0.md`](PREREG_G0.md) §4/§6; IS-only.

---

## Verdict

**STAGE-1 PASS** + operator **B4 GO (2026-08-12)** → G0 [`PREREG_G0.md`](PREREG_G0.md) **FROZEN**. No Pine this turn (CC-solo). No K spend. No TV seat. CONFIRM unread.

**Next:** explore **FALSIFIED 2026-08-13** — [closure](lab/archive/../../docs/briefs/closures/MSL-C2-closure-falsified.md). Hand slot to **P3.2 C3 (M2K)**.

**If explore kills:** registry row + hand slot to **P3.2 C3 (M2K)** — **discharged**.
---

## Iterate

- **Next:** STOP pending explore GO (Pine stays CC-solo after explore PASS).
- **Board write:** plan §6 P3.1 → G0 FROZEN; SESSIONS wrap-up.
