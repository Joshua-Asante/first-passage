# MSL-C3 Stage-1 (K2 revive) — M2K dual-axis MR-at-level (pre-G0)

**Status:** `STAGE-1 PASS` · **B4 paid** → [`PREREG_G0`](PREREG_G0.md) FROZEN → explore **`FALSIFIED`** (both axes) · [closure](../../../docs/briefs/closures/MSL-C3-K2-closure-falsified.md) · Pine not authorized · **$0 · K spent = 0** · G0 `K_intrinsic=2`
**Card:** MSL-C3 revive · instrument **M2K** · scored axes **both** stories below
**Parent:** [election ADR](../../../docs/adr/2026-08-13-msl-c3-k2-dual-axis-revive.md) · [charter](../../../docs/spec/2026-08-12-msl-manual-sourcing-loop-charter.md) steps 2–4 · [slate §MSL-C3](../../../docs/briefs/2026-08-12-msl-first-slate.md) · [STAGE0 PASS](STAGE0.md) · prior [STAGE1](STAGE1.md) (≤1-story; OPERATOR-KILL — historical)
**Evidence CLI:** [`card.yaml`](card.yaml) · [`card_overnight.yaml`](card_overnight.yaml) · [`preflight.json`](preflight.json) · [`preflight_overnight.json`](preflight_overnight.json) (`msl_preflight` — evidence only)

---

## §0 — Why this record exists (re-proposal bar)

| Fact | Owner |
|---|---|
| Original C3 Stage-1 PASSed; B4 declined → OPERATOR-KILL; **no IS score on M2K** | [closure](../../../docs/briefs/closures/MSL-C3-closure-operator-kill.md) |
| Re-proposal bar | fresh Stage-1 + new B4 — not silent revive |
| Same PDH/PDL class explore-FALSIFIED on MYM (C1) | [C1 closure](../../../docs/briefs/closures/MSL-C1-closure-falsified.md) — **adjacency**; does not auto-kill M2K |
| This record | licenses **both** held stories as scored axes at **`K_intrinsic=2`** (DSR floor **0.850**) |

**Cheap falsifier (parent, 2026-08-13):** R/ct $160 vs 4×RT $11.28; all-win $628.72 ≥ $200; all-lose $651.28 ≤ $750 — **PASS** (identical design point for both axes’ arithmetic tables). STAGE0 PROCEED still on disk. `floor_at_k(2)=0.85` reproduced via `PYTHONPATH=lab python3 -c "from research_utils.axis_screen import floor_at_k; print(floor_at_k(2))"`.

---

## Stories — both scored axes (a priori)

| Axis | Story id | Constraint (who loses) | Direction | Not this story |
|---|---|---|---|---|
| A | `pdh-pdl-failed-break-reclaim` | Stops cluster at prior-day **RTH** H/L; failed follow-through forces breakout unwind | Fade failure / reclaim; structural stop beyond swept extreme; truncated-loss; flat 16:00 ET; k=1 first/session | Through-break; OR; overnight reference |
| B | `overnight-range-failed-extension-fade` | Stops cluster at Globex **overnight** H/L; failed extension into RTH forces unwind | Fade failed extension / reclaim; same stop/exit box | PDH/PDL RTH; London/COMEX (C2); WSTRUCT weekly |

**Election rule (this Stage-1 — supersedes the ≤1-story rule in [STAGE1](STAGE1.md) for the revive path only):**

- Both axes are **licensed for IS scoring** after operator explore GO on a dual-axis G0 (`K_intrinsic=2`).
- CONFIRM never used for selection.
- **Delete/flip (Req 1a) mandatory on each axis** before Pine/TV for that axis.
- **Promotion rule (pre-registered):** each axis emits its own explore verdict. Pine/TV may proceed for **at most one** axis:
  - if exactly one is non-`FALSIFIED` under the explore GO gate → that axis;
  - if both clear → higher IS mean net R (long/short pooled mean); tie → Axis A by a priori id order;
  - if both `FALSIFIED` → STOP catalogue (no θ-retune; no silent drop to K=1 rescue).
- A third story = new `K_intrinsic` and a new Stage-1.

**Route (ONE, both axes):** **①** — SLR MR-at-level precedent ([SLR-MYM-1](../../../docs/briefs/closures/SLR-MYM-1-closure-falsified-stage0.md) gate 0-B CLEAR). Not temporal-selectivity; dense-1m pause does not bind this session-scale card.

**CONFIRM window (named before any read; unread through step 8):** `2025-09-01 → 2026-08-13` inclusive.
**IS:** everything before `2025-09-01`. This Stage-1 did **not** read either partition.

**Rejected nearest classes:** see [`MECHANISMS.md`](../../../ops/instruments/MECHANISMS.md) entries for both ids (declared this commit for overnight).

---

## Cost basis (Rule 0)

Tradeify Select 100K Equity Index: `$0.91`/side · tick `$0.50`:

`RT = 2×$0.91 + 2×$0.50 = $2.82` · 4× = **$11.28**/ct ≈ **2.26** RTY pts ($5/pt).

**Design point (both axes, arithmetic tables only):** n=1 entry/day · 4 contracts · stop **32.0 pts** ($160 R/ct) · target 32.0 pts (rr=1 for tables). **`p` / `rr` are not freeze-time claims.** Realized stop distances are explore parameters, not selection axes beyond the two licensed stories.

**K disclosure:** intended G0 `K_intrinsic=2` → screening floor **0.850**. `K_banked(M2K)=0` disclosure-not-gate.

---

## Stage-0 discharge

| Limb | Record |
|---|---|
| L3 one-shot | [STAGE0](STAGE0.md) §1 — brake = declared `K_intrinsic` (here **2** at G0); not a wide search beyond the two frozen stories |
| WSTRUCT sequencing | STAGE0 §2 — SUPERSEDED-ON-COST; discharged; not reopen |
| W4 | STAGE0 §3 — no pull this turn; any later IS path-PnL / Databento needs fresh W4 dry-run |

---

## Step 2 — Dedup + door-check (executed)

### Cell consult (raw)

```
$ python3 scripts/instrument_profiles.py cell M2K pdh-pdl-failed-break-reclaim
... BINDING BAR: index-intraday-ohlcv-directional-timing-2026-07-21 ...
class finding: MYM explore FALSIFIED; M2K unpaid path OPERATOR-KILL; revive in flight (this file)
(exit 1 — BINDING BAR present)

$ python3 scripts/instrument_profiles.py cell M2K overnight-range-failed-extension-fade
... BINDING BAR: index-intraday-ohlcv-directional-timing-2026-07-21 ...
verdict: untested — no prior on this cell.
(exit 1 — BINDING BAR present)
```

Full stdout pinned in [`preflight.json`](preflight.json) / [`preflight_overnight.json`](preflight_overnight.json).

### BINDING BAR / domain answers (both axes)

| Bar / domain item | Route answer |
|---|---|
| `index-intraday-ohlcv-directional-timing-2026-07-21` (M1) | **CLEAR via route ①** — MR-at-level / failed-break reclaim (both reference classes) outside the mapped all-momentum/continuation evidence set. Cite SLR gate 0-B; do not re-argue. |
| Occupancy / S3 | **CLEAR** — M2K never occupied; no rail claim. |
| Stage-0 L3 / WSTRUCT / W4 | **Discharged** — [STAGE0](STAGE0.md) PROCEED. |
| C1 MYM PDH/PDL explore kill | **Adjacency** — does not bind M2K cell; Req 1a still mandatory on Axis A IS; no transfer claim. |
| Dense-1m PDH/PDL θ / CON-5 pause | **Lane-scoped** — does not bind session-scale 15m failed-break reclaim (either reference class). |

### Dedup needles (paste summary)

```
docs/rejected_candidates.md — C3 OPERATOR-KILL row; C1 MYM FALSIFIED; RAISED BAR
docs/briefs/closures/MSL-C3-closure-operator-kill.md — re-proposal = fresh Stage-1 + B4
docs/briefs/closures/MSL-C1-closure-falsified.md — same class × MYM
docs/briefs/closures/SLR-MYM-1-closure-falsified-stage0.md — route ① CLEAR
ops/instruments/M2K.md — M1; WSTRUCT SUPERSEDED; W4 no panel
ops/instruments/MECHANISMS.md — both ids (overnight NEW this commit)
lab/CATALOG.md — msl_c3_m2k_2026-08 ACTIVE
```

---

## Step 3 — $0 screens at RT $2.82 (three kill limbs)

Same design point for both axes (campaign-manager adjudication):

| Limb | Number | Gate | Verdict |
|---|---|---|---|
| cost-law | R/ct **$160** vs 4×RT **$11.28** (tax 0.0176R); 32 pts ≫ 2.26 pt hurdle | gross/trade ≥ $11.28 | **PASS** |
| payability | all-win day **$628.72** | ≥ $200 | **PASS** |
| survival | all-lose day **$651.28** | ≤ $750 | **PASS** |

Disclosures (non-gating): σ_d ≈ $636.79 vs $3,000 trail · implied-SR ≈ **1.60** under placeholder p=0.55 ([report-only ADR](../../../docs/adr/2026-08-13-implied-sr-report-only-fade-reopen.md)) · DSR floor at K=2 = **0.850** (not a Stage-1 kill — gates measured-edge later).

**Clause-N frequency honesty:** designed 1 entry/session/axis ≈ 252/yr design — not rebalance-monthly. Measured rates unpaid until G0 panel (W4). Dual-axis does **not** license 2 entries/session; k=1 still first-valid **per axis per session**, and promotion takes ≤1 axis forward.

---

## Step 4 — Cheap falsifier

1. Cost-law at frozen geometry — **PASS**.
2. Stage-0 + bar answers — **PASS**.
3. Delete/flip unpaid until explore — **mandatory per axis** (IS-only).
   - Axis A DELETE sham: non-prior-day clock level (or overnight H/L) replacing PDH/PDL; FLIP: join extension at reclaim.
   - Axis B DELETE sham: prior-day RTH H/L (or non-overnight clock level) replacing overnight H/L; FLIP: join extension at reclaim.

---

## Verdict

**STAGE-1 PASS** — dual-axis license at `K_intrinsic=2`. **B4 paid** → [`PREREG_G0.md`](PREREG_G0.md) FROZEN → explore **`FALSIFIED`** both axes ([closure](../../../docs/briefs/closures/MSL-C3-K2-closure-falsified.md) · [`RESULTS_g2`](RESULTS_g2.md)). No Pine. CONFIRM unread.

**Next:** STOP this G0. Board slot freed — **S2B** may resume.

---

## Iterate

- **Next:** STOP / Board (S2B). Explore artifact: [`RESULTS_g2.md`](RESULTS_g2.md).
- **Board write:** plan §6 P3.2b C3-K2 explore FALSIFIED · S2B unblocked.
