# MSL-S2A Stage-1 — MCL pullback-failure resumption (pre-G0)

**Status:** `STAGE-1 PASS` · **B4 PAID 2026-08-13** · G0 **FROZEN** ([`PREREG_G0.md`](PREREG_G0.md)) · explore **`FALSIFIED`** ([`RESULTS_g2`](RESULTS_g2.md)) · Pine not authorized · **$0 · K=0**
**Card:** MSL-S2A · instrument **MCL** · elected mechanism **`pullback-failure-resumption`** (NEW)
**Parent:** [MSL charter](../../../docs/spec/2026-08-12-msl-manual-sourcing-loop-charter.md) steps 2–4 · [second slate §S2A](../../../docs/briefs/2026-08-13-msl-second-slate.md) · [STAGE0 PASS](STAGE0.md) · [design-box ADR](../../../docs/adr/2026-08-13-msl-slate-2-design-box.md) · [implied-SR report-only](../../../docs/adr/2026-08-13-implied-sr-report-only-fade-reopen.md)
**Evidence CLI:** [`card.yaml`](card.yaml) · [`preflight.json`](preflight.json) (`msl_preflight` — evidence only)

---

## Freeze (zero data contact)

| Field | Frozen value |
|---|---|
| Trigger class (one) | *Pullback-failure resumption* — join an established intraday directional move after a pullback fails to reverse it; entry on the resumption bar |
| Stop / target | Hard stop beyond the pullback extreme; target at **rr = 3** of that stop (box `[2, 3]`; rr is geometry, not a measured-edge claim) |
| Cadence | k=1; first valid signal per session; no pyramiding |
| Not chosen | Breakout-from-range; compression-expansion; MR-at-level; TAS/settlement; CONFIG-B fade; OR continuation |

**WHO (Req 1a):** in a directionally-committed session, participants who faded the move hold losing inventory; a pullback that fails to extend forces that inventory out — the unwind is the continuation leg. The constraint (established direction **∧** failed pullback) must SELECT the trade. A bare “momentum continues” story is not admissible.

**CONFIRM window (named before any read; unread through step 8):** `2025-07-01 → 2026-07-02` (panel end — not “today”).
**IS:** everything before `2025-07-01`. This Stage-1 pass did **not** read either partition. Panel bytes absent in this clone; hash pin in [STAGE0](STAGE0.md).

**Rejected nearest classes** (also in `MECHANISMS.md`):
- `opening-range-continuation` / `opening-pressure` — OR continuation; dead on MYM
- `pdh-pdl-breakout-rth` — through-break; not pullback-failure
- `impulse-pullback-vwap-reclaim` — CON-5 VWAP reclaim; paused dense-1m lane
- `compression-gated-breakout` / `htf-compression-breakout-5m` — second trigger class, not licensed
- `trend-following` — USOIL regime-capture; no pullback-failure constraint
- `mean-reversion-fade` — USOIL spike-fader; opposite direction
- `event-window-reversal` / Q-MCLTAS-1 — TAS/settlement; different modality
- `london-range-failed-extension-fade` / `pdh-pdl-failed-break-reclaim` — slate-1 MR-at-level; opposite family

---

## Session window (W3) — named before any read

**Card-scoped ruling, does not close the fade-program’s still-open session-window question** ([frozen rulings](../../../docs/notes/2026-07-31-fade-stage1-frozen-rulings.md) “Which session window governs MCL integrity”).

| Limb | Ruling |
|---|---|
| Window | **09:00–14:30 ET** |
| End | **14:30 ET** — close of the CL settlement-determination period (14:28–14:30 ET). Flat by 14:30, **not** 16:00 equity close (W3). |
| Start | **09:00 ET** — comparability pin with the fade Stage-0 integrity battery on this instrument. Disclosed as a **dead NYMEX-floor artefact**, not a CME-published RTH (MCL launched 2021-07-12; pit was already gone). |
| FOMC (W4) | FOMC days **excluded** (intent recorded here; calendar frozen at G0). Does not re-use the fade 180→120 min τ_max as a hold-horizon — this card’s stop is structural at the pullback extreme. |

A second window that reached scoring would charge `K_intrinsic` +1.

---

## Roll exclusion (W1) — declared, not yet applied

Adopt **`ROLL-EXCLUDE-2026-07-31`** identically on IS and CONFIRM (same 2-session lead window). Disclose the MCL-paid rate **~14%** session exclusion (not the 4.65% quarterly figure the ruling published for index micros). **Calendar frozen at G0** — see [`PREREG_G0.md`](PREREG_G0.md) §1 (162 excluded session dates). Designed 1 entry/session still clears N-ACT ≥1/week after a 14% cut; **measured** rate unpaid until explore.

---

## Cost basis (Rule 0)

Tradeify Select 100K Energy, priced as the MGC comment pin (second slate; `firm_rules` comment “MGC=$1.06”; MCL tick value **$1.00**):

`RT = 2×$1.06 + 2×$1.00 = $4.12` · 4× hurdle = **$16.48**/contract/trade.

**Design point:** n=1 entry/day · **2 contracts** · stop **180 ticks** ($180 R/ct) · target 540 ticks (rr=3). Rounded from re-derivation frontier **$177.1** at p=0.35 / rr=3 / c=$4.12; Magdon-Ismail does **not** recalibrate this. **`p` is not a freeze-time claim.**

40% consistency at this point: one-win day $1,071.76 / $6,000 = **17.9%** — under the 40% line.

---

## Stage-0 discharge

| Limb | Record |
|---|---|
| SNAG bar on MCL | [STAGE0](STAGE0.md) §1 — registered; door-check non-vacuous |
| Panel pin | STAGE0 §2 — `SHA256SUMS` `5aa50456…bbd23`; bytes absent this clone |
| Box election | [ADR](../../../docs/adr/2026-08-13-msl-slate-2-design-box.md) Accepted; Magdon-Ismail not calibration |

---

## Step 2 — Dedup + door-check (executed)

### Cell consult (raw)

```
$ python3 scripts/instrument_profiles.py cell MCL pullback-failure-resumption
=== MCL x pullback-failure-resumption ===
ledger: ops/instruments/MCL.md
verdict: untested — no prior on this cell.
class finding (mechanism-wide, not specific to MCL): none yet — Stage-1 on MCL; B4/G0 unpaid. [STAGE1](...)
BINDING BAR: free-data-5th-leg-snag-closed-2026-07-01 -> ../../docs/rejected_candidates.md
cost hurdle: 5.3423 bp/round-trip (Stage-0 2023 median cost_bp for MCL …) — VERIFY at #C1
K bank: read ../../discovery_manifests/ — never trust a snapshot.
prior: Frozen CONFIG-B-MCL geometry clears expressibility under SIGMA-NATIVE; geometry is not edge — N-SURV/N-EDGE/N-SIZE remain U until a mechanism trade series exists. [#C2]
(exit 1 — BINDING BAR present; campaign manager answers the bar below)
```

### BINDING BAR answers

| Bar / domain item | Route answer |
|---|---|
| `free-data-5th-leg-snag-closed-2026-07-01` | **CLEAR by domain mismatch** under ratified **R-FRAMING = §2.1**: Tradeify-native survival construct sits outside free-data 5th-leg SNAG scope (within-strategy alpha / free-exogenous regime gates / published-retail / chop-native decorrelated legs). S2A is not a 5th-leg expansion candidate. Not walking the three re-proposal routes. |
| Index intraday OHLCV raised bar | **Does not bind** — MCL is not an equity-index future (Stage-0 omitted it on purpose). Continuation/momentum being the bar’s exhausted lever on *index* OHLCV is why this card is on MCL. |
| R-FRAMING status | **§2.1 governs** (Board B1); recorded here as the card line. |
| Occupancy | **CLEAR** — MCL never occupied; no rail claim. B8 is MYM/MNQ-only. Energy Product Group; Striker redeploy bar does not bind this symbol. |

### Dedup `rg` (mechanism family + role) — paste

Needle set: pullback-failure / session-trend / CONFIG-B-MCL / Q-MCLTAS / spike-fader / opening-range-continuation / impulse-pullback-vwap.

`msl_preflight` needle `pullback-failure-resumption` → **0 hits** (no prior of this construct). Broader family+role sweep (executed this session):

```
docs/briefs/2026-08-13-msl-second-slate.md — MSL-S2A card (this campaign)
docs/briefs/closures/Q-MCLTAS-1-closure-falsified.md — TAS/settlement magnitude; different modality
docs/rejected_candidates.md — USOIL spike-fader (fade entry); tas-settlement-window-replication on MCL (not this family)
ops/instruments/MCL.md — CONFIG-B-MCL fade geometry (not this mechanism); SNAG bar this commit
ops/instruments/MECHANISMS.md — opening-range-continuation; impulse-pullback-vwap-reclaim; this id NEW
lab/CATALOG.md — no prior pullback-failure-resumption row
```

### Adjacencies (not bars)

- **Q-MCLTAS-1** — TAS/settlement FALSIFIED on magnitude; different modality. Do not borrow δ or re-proposal bar.
- **CONFIG-B-MCL-2026-07-31** — frozen **fade** geometry, mechanism-owed. This card is not that config.
- **USOIL spike-fader** — fade entry, CFD-era, different venue/symbol; ledger says do not inherit.
- **BE3/SFX-1** — fade-census kills, fade-scoped 2026-08-10.
- **Slate-1 C1/C2** — MR-at-level at rr≈1; opposite family. C1 DELETE PASS is S2B’s asset, not this card’s.

---

## Step 3 — $0 screens at RT $4.12 (three kill limbs)

Campaign-manager adjudication (not the CLI):

| Limb | Number | Gate | Verdict |
|---|---|---|---|
| cost-law | R/ct = **$180** vs 4×RT **$16.48** (tax 4.12/180 = 0.023R); tool expectancy-conditioned 4× floor $41.20 at placeholder p=0.35 | gross/trade ≥ $16.48 | **PASS** |
| payability | all-win day = **$1,071.76** (= 2×(540 − 4.12)) | ≥ $200 | **PASS** |
| survival | all-lose day = **$368.24** (= 2×(180 + 4.12)) | ≤ $750 | **PASS** |

Disclosures (non-gating): σ_d ≈ **$686.84** vs $3,000 trail · implied-SR ≈ **3.33** under placeholder p=0.35 / rr=3 / n=1 (evidence only; not a kill — [`ADR 2026-08-13`](../../../docs/adr/2026-08-13-implied-sr-report-only-fade-reopen.md)) · 40% consistency 17.9% · $180 is $3 above diffusion R_max $177.1 (re-derivation §3 @ MGC/MCL c=$4.12); Magdon-Ismail validation does not recalibrate.

**Entry-rate / N-ACT honesty:** designed 1 entry/session ≈ 252 events/yr, ~14% roll-exclude still ≫ 1/week. **If measured rate < ~1/week, N-ACT FAILS as a solo construct: kill or redesign, don’t disclose.** Measured rate unpaid until G0.

---

## Step 4 — Cheap falsifier

1. **Cost-law at frozen geometry** — PASS ($180 ≫ $16.48). Did not invent `p` to rescue.
2. **Adjacency scope** — freeze is neither TAS, CONFIG-B fade, USOIL spike-fader, nor slate-1 MR-at-level — PASS.
3. **Session window named before any read** — 09:00–14:30 ET recorded above — PASS.
4. **Panel / CONFIRM bound** — CONFIRM ends 2026-07-02; no peek — PASS. Bytes absent this clone; no IS read attempted.
5. **Delete/flip (Req 1a)** — unpaid at Stage-1 arithmetic; **mandatory before Pine/TV** on the elected story (IS-only). Sham for DELETE: a random in-session bar at matched time-of-day (slate). FLIP: join the pullback instead of its failure.

---

## Verdict

**STAGE-1 PASS** on elected story `pullback-failure-resumption`. **B4 paid** — G0 frozen. Explore **`FALSIFIED`** (N-ACT). No Pine. No K spend. CONFIRM unread.

**Next:** STOP this G0. S2B route still unresolved.

---

## Iterate

- **Next:** STOP — [closure](../../../docs/briefs/closures/MSL-S2A-closure-falsified.md).
- **Board write:** plan §6 P3.4 → **FALSIFIED** (explore IS).
