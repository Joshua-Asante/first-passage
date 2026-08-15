# MSL-S2B Stage-1 — MYM sweep-failure-filtered continuation (pre-G0)

**Status:** `STAGE-1 FAIL` (route) · G0 **never frozen** · B4 **unpaid** · Pine not authorized · **$0 · K=0**
**Card:** MSL-S2B · instrument **MYM** · elected mechanism **`sweep-failure-filtered-continuation`** (NEW)
**Parent:** [MSL charter](../../../docs/spec/2026-08-12-msl-manual-sourcing-loop-charter.md) steps 2–4 · [second slate §S2B](../../../docs/briefs/2026-08-13-msl-second-slate.md) · [STAGE0 PASS](STAGE0.md) · [design-box ADR](../../../docs/adr/2026-08-13-msl-slate-2-design-box.md) · [B8 occupancy](../../../docs/adr/2026-08-12-msl-mym-occupancy-release.md)
**Evidence CLI:** [`card.yaml`](card.yaml) · [`preflight.json`](preflight.json) (`msl_preflight` — evidence only)
**Closure:** [`MSL-S2B-closure-stage1-fail-route.md`](../../../docs/briefs/closures/MSL-S2B-closure-stage1-fail-route.md)

---

## Freeze (zero data contact)

| Field | Frozen value |
|---|---|
| Trigger class (one) | *Sweep-failure-filtered continuation* — trend-continuation entry on MYM **gated** by PDH/PDL sweep-failure; sweep-failure is a **filter, never the entry** |
| Stop / target | Hard stop; target at **rr ∈ [2, 3]** of that stop (box geometry, not a measured-edge claim) |
| Cadence | k=1; first valid signal per session; no pyramiding; flat by 16:00 ET |
| Not chosen | PDH/PDL failed-break **reclaim entry** (C1); OR continuation; through-break; bare momentum |

**WHO (Req 1a):** continuation entry only when the session has already swept and failed a prior-day extreme — the filter selects the subset; the entry remains trend-continuation. C1 DELETE PASS (constrained mean > overnight sham on both arms) is the **filter-role asset**; C1 primary FALSIFIED does not rescue.

**CONFIRM window (named before any read; unread):** `2025-09-01 → panel end` (MYM.md M7 ends **2026-07-03Z** — not “today”).
**IS:** everything before `2025-09-01`. This Stage-1 record did **not** read either partition. Panel bytes may be absent in this clone; hash pin in [STAGE0](STAGE0.md).

**Rejected nearest classes** (also in `MECHANISMS.md`):
- `pdh-pdl-failed-break-reclaim` — C1 entry-role FALSIFIED; not a silent reopen
- `opening-range-continuation` / `opening-pressure` — OR continuation; dead on MYM
- `pdh-pdl-breakout-rth` — through-break (CON-4); opposite selector
- `ict-liquidity` / SLR-MYM-1 — sweep-as-entry; Stage-0 FALSIFIED as scoped
- `pullback-failure-resumption` — S2A continuation without this filter; FALSIFIED N-ACT on MCL
- `impulse-pullback-vwap-reclaim` — CON-5; paused dense-1m lane
- `trend-following` / `band-pierce-continuation` — no sweep-failure filter
- `mean-reversion-fade` — USOIL spike-fader entry; role-asymmetry does not auto-clear

---

## Cost basis (Rule 0) — disclosed only

Tradeify Select 100K index-micro RT **$2.82** · 4× hurdle **$11.28**/contract/trade.
`card.yaml` placeholder geometry (evidence tables only): stop **40 pts** · rr=3 · 2 contracts · `$0.50`/pt. **Not adjudicated** — route FAIL stops before Step 3.

---

## Stage-0 discharge

| Limb | Record |
|---|---|
| Rule-8 dedup paste | [STAGE0](STAGE0.md) §0 — no live S2B camp |
| Panel / CONFIRM pins | STAGE0 §2–3 — `SHA256SUMS` `24e16952…97a58`; IS/CONFIRM named unread |
| Mechanism draft | `sweep-failure-filtered-continuation` NEW |
| SNAG registration | **N/A** — MYM already carries raised bar |
| Occupancy | B8 cite — research/G0 allowed; Striker redeploy bar stands |

---

## Step 2 — Dedup + door-check (executed)

### Cell consult (raw)

```
$ python3 scripts/instrument_profiles.py cell MYM sweep-failure-filtered-continuation
=== MYM x sweep-failure-filtered-continuation ===
ledger: ops/instruments/MYM.md
venue: NOT TRADABLE at the live firm — AUTHORIZED-but-venue-less incumbent (Striker DJ30 MYM edition); no live book to correlate new work against — check venue_note before book-correlation gate.
verdict: untested — no prior on this cell.
class finding (mechanism-wide, not specific to MYM): Stage-1 **FAIL** (route) — index raised bar unbound for continuation *entry*; SLR route ① clears MR-at-level *filter* only; temporal-selectivity route blocked by Q-TNEC-CON-5 pause; composite clearance forbidden. [STAGE1](…) · [closure](…). $0 / K=0; G0 never frozen.
BINDING BAR: index-intraday-ohlcv-directional-timing-2026-07-21 -> ../../docs/rejected_candidates.md
BINDING BAR: index-intraday-ohlcv-directional-timing-2026-07-21 -> ../../docs/rejected_candidates.md
cost hurdle: 6.57 bp/event (4x Tradeify hurdle) — VERIFY at #M6
K bank: read ../../discovery_manifests/ — never trust a snapshot.
prior: Not a barren instrument — the incumbent locked leg is profitable here; one narrow continuation expression failed. [#M1]
(exit 1 — BINDING BAR present; campaign manager answers the bar below)
```

`cell_returncode=1` is expected whenever a BINDING BAR is present (`instrument_profiles.cmd_cell`);
preflight still exits 0 (evidence only).

### BINDING BAR / domain answers — **kill limb #1 first**

| Bar / domain item | Route answer |
|---|---|
| `index-intraday-ohlcv-directional-timing-2026-07-21` | **FAIL.** Entry is trend-continuation — the bar’s **named exhausted lever** (price / cross-instrument-selection / hold-time mapped set). Evaluated **only** the two slate-named candidates: **(A) SLR route ①** — CLEAR for MR-at-level *filter signal* ([SLR-MYM-1 closure](../../../docs/briefs/closures/SLR-MYM-1-closure-falsified-stage0.md) gate 0-B); does **not** clear continuation *entry* (slate + C1 precedent cite-don’t-re-argue). **(B) Within-instrument temporal selectivity** ([ADR 2026-08-10](../../../docs/adr/2026-08-10-temporal-selectivity-outside-mapped-levers.md)) — route ① *could* open under §2-B, but the dense-1m OHLCV temporal-selectivity lane is **default-paused** ([Q-TNEC-CON-5](../../../docs/briefs/closures/Q-TNEC-CON-5-closure-ambiguous-hold.md) Branch A, 2026-08-12); no Board un-pause and no explicit non-route-① thesis on this card. **Forbidden composite refused:** “filter clears via route ① ⇒ continuation entry CLEAR.” |
| Occupancy / S3 | **CLEAR via B8** — [`ADR 2026-08-12`](../../../docs/adr/2026-08-12-msl-mym-occupancy-release.md): `MYM1!` released for new non-Striker MSL research/G0. S1 keep-warm + Striker redeploy bar stand. PROFILE `venue_tradable: false` is Striker-withdrawn posture, not an MSL research ban. |
| Dense-1m “forbids PDH/PDL θ” | **Lane-scoped — does not bind** this card’s *filter* reference (session-scale 15m; not a new dense-1m CON-4 through-break family). Re-verified; does not rescue the raised-bar FAIL above. |
| R-FRAMING | **§2.1 governs** (Board B1); MYM is an index — raised bar still binds; §2.1 does not waive it. |

### Dedup `rg` (mechanism family + role) — paste

Needle set: sweep-failure / pdh-pdl-failed-break / opening-range-continuation / temporal-selectivity / index-intraday-ohlcv / SLR-MYM.

`msl_preflight` needle `sweep-failure-filtered-continuation` → **1 hit** (this id’s `MECHANISMS.md` header — expected at card commit). Broader family+role sweep (executed this session):

```
docs/briefs/2026-08-13-msl-second-slate.md — MSL-S2B card (this campaign)
docs/briefs/closures/MSL-C1-closure-falsified.md — entry-role FALSIFIED; DELETE PASS = filter asset
docs/briefs/closures/SLR-MYM-1-closure-falsified-stage0.md — route ① CLEAR for MR-at-level only
docs/briefs/closures/Q-TNEC-CON-5-closure-ambiguous-hold.md — temporal-selectivity lane default PAUSED
docs/rejected_candidates.md — raised bar; C1/C3 pdh-pdl-failed-break-reclaim rows
ops/instruments/MYM.md — opening-range-continuation DEAD; raised bar wired; C1 journal
ops/instruments/MECHANISMS.md — this id NEW; rejected nearest listed
lab/CATALOG.md — no prior msl_s2b row (camp opens this commit)
```

### Adjacencies (not bars)

- **MSL-C1** — entry-role dead; DELETE PASS is filter evidence only; do not re-run entry.
- **Opening-range continuation on MYM** — DEAD, seven gates.
- **Q-TXG-1** — transfer/expression lane FALSIFIED-at-walls; re-proposal = different loss-side shape / venue-class — not this card’s clearance path.
- **S2A** — continuation without this filter; different instrument; FALSIFIED N-ACT.

---

## Step 3 — $0 screens

**Not reached.** Route kill limb #1 FAIL stops the card before arithmetic adjudication (plan: skip forcing screens to look complete). Evidence tables remain in [`preflight.json`](preflight.json) for the record only.

---

## Step 4 — Cheap falsifier

**Not reached.** Same stop.

Named for the record (unexecuted): Req 1a on the **filter** would require filtered continuation to beat an **unfiltered** continuation baseline on IS only — sham/FLIP unpaid; moot under route FAIL.

---

## Verdict

**STAGE-1 FAIL** on elected story `sweep-failure-filtered-continuation` — **route declaration (kill limb #1)**. Pre-G0 kill at $0. No B4. No G0. No Pine. No K spend. CONFIRM unread.

**Correct outcome** per second-slate: *“If Stage 1 cannot answer the bar by a route that already exists, this card is a $0 pre-G0 kill.”*

---

## Iterate

- **Next:** STOP this card.
- **Board write:** plan §6 P3.5 S2B → **STAGE-1 FAIL (route)** · Stage-1 deaths **1/3 → 2/3** · slate-2 exhausted on both cards.
- **Re-proposal:** new modality / Board un-pause of temporal-selectivity with an explicit non-route-① thesis / different loss-side shape — **not** θ-retune, not composite clearance, not silent reopen of C1 entry.
