# MSL-C3 Stage-1 — M2K PDH/PDL failed-break reclaim (pre-G0)

**Status:** `STAGE-1 PASS` · **B4 DECLINED 2026-08-13** → [`OPERATOR-KILL`](../../../docs/briefs/closures/MSL-C3-closure-operator-kill.md) · G0 not frozen · Pine not authorized · **$0 · K=0**
**Card:** MSL-C3 · instrument **M2K** · elected mechanism **`pdh-pdl-failed-break-reclaim`** (NEW)
**Parent:** [MSL charter](../../../docs/spec/2026-08-12-msl-manual-sourcing-loop-charter.md) steps 2–4 · [slate §MSL-C3](../../../docs/briefs/2026-08-12-msl-first-slate.md) · [STAGE0 PASS](STAGE0.md) · [implied-SR report-only](../../../docs/adr/2026-08-13-implied-sr-report-only-fade-reopen.md)
**Evidence CLI:** [`card.yaml`](card.yaml) · [`preflight.json`](preflight.json) (`msl_preflight` — evidence only)

> **Historical record only.** Revive path = [`STAGE1_K2.md`](STAGE1_K2.md) + [ADR 2026-08-13](../../../docs/adr/2026-08-13-msl-c3-k2-dual-axis-revive.md) (`K_intrinsic=2`, both stories scored). Do not treat this file’s ≤1-story election as the live license.

---

## Stories frozen before data contact (authoring order = priority for delete/flip election)

| Pri | Story id | Constraint (who loses) | Direction | Not this story |
|---|---|---|---|---|
| **1 (elected)** | `pdh-pdl-failed-break-reclaim` | Stops cluster at prior-day RTH H/L; a sweep that **fails** to follow through forces the breakout cohort to unwind | Fade the **failure** (reclaim after non-follow-through); structural stop beyond swept extreme; truncated-loss; flat by 16:00 ET; k=1 first valid/session | Through-break (`pdh-pdl-breakout-rth`); OR continuation; overnight reference |
| 2 (held) | `overnight-range-failed-extension-fade` | Globex overnight H/L as the visible stop cluster; failed extension into RTH forces unwind | Fade failed extension / reclaim; same stop/exit box | PDH/PDL; London/COMEX (C2); WSTRUCT weekly |

**Election rule (frozen with stories):** score delete/flip on IS in priority order; **≤1 story** may reach scoring / G0. Story 2 stays unread until story 1 dies at Stage-1 / explore / operator kill. Extra scored story would charge `K_intrinsic` +1 — not licensed here.

**Route (ONE, recorded):** **①** — SLR MR-at-level precedent ([SLR-MYM-1 closure](../../../docs/briefs/closures/SLR-MYM-1-closure-falsified-stage0.md) §2 gate 0-B: route 1 **clears**; Stage-0 kill was framing delete/flip + day-set N, not the bar). Not temporal-selectivity; dense-1m pause ([Q-TNEC-CON-5](../../../docs/briefs/closures/Q-TNEC-CON-5-closure-ambiguous-hold.md)) does not bind this session-scale MR-at-level card.

**CONFIRM window (named before any read; unread through step 8):** `2025-09-01 → 2026-08-13`.
**IS:** everything before `2025-09-01`. This Stage-1 pass did **not** read either partition.

**Rejected nearest classes** (also in `MECHANISMS.md`):
- `pdh-pdl-breakout-rth` — through-break continuation (CON-4); opposite selector
- `opening-range-continuation` / `opening-pressure` — OR continuation / pressure; dead on MYM
- `ict-liquidity` — SLR-MYM-1 class home; ICT weekly-gated first-30m sweep — different framing; Stage-0 FALSIFIED as scoped
- `london-range-failed-extension-fade` — C2 MGC; metals London/COMEX; FALSIFIED explore
- `mean-reversion-fade` — generic USOIL spike-fader; no PDH/PDL failure constraint
- WSTRUCT weekly-structure — SUPERSEDED-ON-COST; not this session-scale card ([STAGE0](STAGE0.md))

---

## Cost basis (Rule 0)

Tradeify Select 100K Equity Index: `$0.91`/side · tick `$0.50` · 1 tick/side slip (fade-spec / slate):

`RT = 2×$0.91 + 2×$0.50 = $2.82` · 4× hurdle = **$11.28**/contract/trade ≈ **2.26** RTY pts ($5/pt).

**Design point (elected story):** n=1 entry/day · 4 contracts · stop **32.0 pts** ($160 R/ct) · target 32.0 pts (rr=1 for geometry tables only). **`p` / `rr` are not freeze-time claims.**

---

## Stage-0 discharge (kill-list item)

| Limb | Record |
|---|---|
| L3 one-shot | [STAGE0](STAGE0.md) §1 — family one-shot void; brake = `K_intrinsic=1`; disclosure `K_banked(M2K)=0` |
| WSTRUCT sequencing | STAGE0 §2 — SUPERSEDED-ON-COST; sequenced **discharged**; not reopen |
| W4 | STAGE0 §3 — no pull; Stage-1 arithmetic panel-free |

---

## Step 2 — Dedup + door-check (executed)

### Cell consult (raw)

```
$ python scripts/instrument_profiles.py cell M2K pdh-pdl-failed-break-reclaim
=== M2K x pdh-pdl-failed-break-reclaim ===
ledger: ops/instruments/M2K.md
verdict: untested — no prior on this cell.
class finding (mechanism-wide, not specific to M2K): none yet — Stage-1 PASS on M2K; B4/G0 unpaid. [STAGE1](...)
BINDING BAR: index-intraday-ohlcv-directional-timing-2026-07-21 -> ../../docs/rejected_candidates.md
cost hurdle: 11.89 bp/round-trip (panel-era median …) — VERIFY at #M2
K bank: read ../../discovery_manifests/ — never trust a snapshot.
prior: Cross-index RV selection … [#M3]
prior: Opening-range momentum is an equity-index property … [#M4]
(exit 1 — BINDING BAR present; campaign manager answers the bar below)
```

### BINDING BAR answers

| Bar / domain item | Route answer |
|---|---|
| `index-intraday-ohlcv-directional-timing-2026-07-21` (M1) | **CLEAR via route ①** — mean-reversion-at-a-level / failed-break reclaim sits outside the mapped all-momentum/continuation cost-ratio evidence set. Cite SLR-MYM-1 gate 0-B clearance (surviving); do not re-argue. Not route ② (modality) or ③ (beat ORB-MNQ). |
| Occupancy / S3 | **CLEAR** — M2K never occupied; no rail claim. B8 is MYM/MNQ-only. |
| Stage-0 L3 / WSTRUCT / W4 | **Discharged** — [STAGE0](STAGE0.md) PROCEED. |

### Dedup `rg` (mechanism family + role) — paste

Needle set: PDH/PDL / failed-break / reclaim / M2K / SLR / overnight-range / WSTRUCT / raised bar / opening-range.

```
docs/briefs/2026-08-12-msl-first-slate.md — MSL-C3 card (this campaign); C1 PDH/PDL on MYM (sibling instrument, not this cell)
docs/briefs/closures/SLR-MYM-1-closure-falsified-stage0.md — Stage-0 FALSIFIED (framings + day-set); route 1 CLEARS
docs/rejected_candidates.md — RAISED BAR 2026-07-21; OR continuation MYM; cross-index RV
ops/instruments/M2K.md — M1 bar; BE1 VWAP DEAD; PROPENG BLOCKED; WSTRUCT SUPERSEDED-ON-COST
ops/instruments/MECHANISMS.md — pdh-pdl-breakout-rth (through-break); london-range-failed-extension-fade (C2 FALSIFIED)
lab/CATALOG.md — msl_c3_m2k_2026-08 ACTIVE; wstruct_cost_geometry; msl_c2 FALSIFIED
```

`msl_preflight` needle `pdh-pdl-failed-break-reclaim` → see [`preflight.json`](preflight.json).

### Adjacencies (not bars)

- **SLR-MYM-1** — mechanism never tested; framings failed delete/flip. C3’s PDH/PDL *failure* constraint must still survive Req 1a on IS (mandatory before Pine) — Stage-1 does not claim SLR was rescued.
- **MSL-C1** — same reference class on MYM; serialized after C3; not a scored transfer; instrument election is independent.
- **BE1 / PROPENG on M2K** — DEAD / BLOCKED; not this construct.
- **C2 London-range** — FALSIFIED on MGC; different instrument + reference class.

---

## Step 3 — $0 screens at RT $2.82 (three kill limbs)

Campaign-manager adjudication (not the CLI):

| Limb | Number | Gate | Verdict |
|---|---|---|---|
| cost-law | R/ct = **$160** vs 4×RT **$11.28** (tax 2.82/160 = 0.0176R); span 32 pts ≫ 2.26 pt hurdle | gross/trade ≥ $11.28 | **PASS** |
| payability | all-win day = **$628.72** (= 4×160 − 4×2.82) | ≥ $200 | **PASS** |
| survival | all-lose day = **$651.28** (= 4×160 + 4×2.82) | ≤ $750 | **PASS** |

Disclosures (non-gating): σ_d ≈ $636.79 vs $3,000 trail · implied-SR ≈ **1.60** under placeholder p=0.55 (evidence only; not a kill — [`ADR 2026-08-13`](../../../docs/adr/2026-08-13-implied-sr-report-only-fade-reopen.md)). Tool also prints expectancy-conditioned stop floor 4×RT/E[R] ≈ $112.80 (22.56 pts) at that placeholder — design stop **32 pts / $160** clears both the slate raw 4×RT and the tool floor.

**Clause-N frequency honesty:** designed 1 entry/session ≈ 252 events/yr — **not** rebalance/D3/D7 monthly-dead. Measured confirm-power unpaid until a G0 panel exists (W4).

---

## Step 4 — Cheap falsifier

1. **Cost-law at frozen geometry** — PASS ($160 ≫ $11.28). Did not invent `p` to rescue.
2. **Stage-0 + adjacency scope** — STAGE0 PROCEED; not WSTRUCT reopen / BE1 / PROPENG / C2 London — PASS.
3. **Delete/flip (Req 1a)** — unpaid at Stage-1 arithmetic; **mandatory before Pine/TV** on the elected story (IS-only). Sham reference for DELETE: replace PDH/PDL with prior Globex-day RTH H/L (or a non-prior-day clock level) while keeping reclaim/stop/target; FLIP: join the extension at the same reclaim bar.

---

## Verdict

**STAGE-1 PASS** on elected story `pdh-pdl-failed-break-reclaim`. **B4 DECLINED 2026-08-13** — [OPERATOR-KILL closure](../../../docs/briefs/closures/MSL-C3-closure-operator-kill.md). No G0. No Pine. No K spend. CONFIRM never reserved for a freeze. Story 2 held unread.

**Next:** slot → **P3.3 C1 (MYM)**.

---

## Iterate

- **Next:** STOP — operator kill; handoff C1.
- **Board write:** plan §6 P3.2 → OPERATOR-KILL; Stage-1 deaths 1/3; P3.3 NEXT.
