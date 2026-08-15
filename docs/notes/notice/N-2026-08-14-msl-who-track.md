# NOTICE 2026-08-14 — MSL WHO-track (estate-wide; still dry)

**Notice ID:** N-2026-08-14-msl-who-track
**Observed:** 2026-08-14
**Author:** Cursor (E1 HOLD follow-on; operator: “deep research track for the new WHO”)
**Type:** Notice-phase. Zero-data WHO sweep. $0 · K=0 · no camp · no card.
**Status:** `HELD` — **STILL DRY.** E1 stop rule stands: no slate-4 card until a NEW WHO.
**Trigger:** [E1 HOLD](../../briefs/closures/MSL-S7-closure-resolved-e1-hold.md) — Phase 3 paused until a constraint-based WHO that is **not** in the 2026-08-10 INTAKE-DRY set and **not** a transfer of C1/C2/C3/S2A/S2B. Slate-3 only swept **fade × MCL**. This track sweeps the rest of the Tradeify envelope.

---

## §0 — Source anchor

- **Source:** E1 stop rule + operator direction to run the WHO track. Production / doctrine reads this session @ `39b17d41` (merge of [PR #821](https://github.com/Joshua-Asante/first-passage/pull/821)).
- **Observed at:** 2026-08-14 (same calendar day as E1; letter **n**).

| Path | Anchor |
|---|---|
| [E1 closure](../../briefs/closures/MSL-S7-closure-resolved-e1-hold.md) | `39b17d41` |
| [plan](../../briefs/2026-08-12-msl-program-plan.md) §4/§6 | `53d91873` |
| [slate-3 notice](N-2026-08-14-msl-slate-3-constraints.md) | `c4dc069d` |
| [census](N-2026-07-26-forced-flow-census.md) pass 3 backlog + pass 4 | standing |
| [ADR 2026-07-26 §2-A](../../adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md) | four clauses |
| [charter](../../spec/2026-08-12-msl-manual-sourcing-loop-charter.md) step 1 | `8290b895` |
| [harvest Req 1a](../../methodology/strategy_harvest.md) §5 | four clauses |
| [`MCL.md`](../../../ops/instruments/MCL.md) 2026-08-10 INTAKE-DRY | `5f7af2c3` |
| [`M6A.md`](../../../ops/instruments/M6A.md) envelope NON-EMPTY / no mechanism | 2026-08-11 |
| [envelope §4a](../../../ops/prop_envelope_default.md) product groups | 2026-07-22 |
| [`firm_rules.py`](../../../core/firm_rules.py) `Tradeify_Select_100K` | no M6J; Treasuries venue-dead; grains + EUREX rates listed |

**Rule-8** (paste, this session — `msl_s4` / `s4a` / `who-track` / `slate-4` / `NEW WHO` / `msl-who` on `lab/CATALOG.md` + `docs/briefs/INDEX.md`):

```
# lab/CATALOG.md
(empty)

# docs/briefs/INDEX.md
(empty)

# camps
$ test ! -d lab/analysis/c1/msl_s3a_mcl_2026-08 && test ! -d lab/analysis/c1/msl_s4a_mcl_2026-08
no s3a/s4a camps
```

`check_advisor_dedup.py --keywords "msl who-track new who slate-4 grains bund option-cut FGBL cancelled-warrant"`: **no slug collision.** Keyword hits are unrelated audits (`option`/`slate`/`track`).

**Cheap falsifier (parent-side, generous):** a NEW WHO already named on `origin/main`, or a grain/Bund/option-cut card already in the registry, would make this track a re-derivation. **Neither exists.** Grains/EUREX rates appear on the envelope and in the Treasury venue-bar note; no WHO was authored against them.

---

## §1 — The observation

Slate-3 recorded dryness **inside** the reopened MCL fade geometry. E1 then forbade a slate-4 card until a WHO outside that well and outside the five spent MSL families. A zero-data walk of every Tradeify product group, the census pass-3 backlog, and the closest 1a-shaped leftovers still cannot name a WHO that survives delete/flip.

---

## §2 — Why it stands out

- **Baseline:** E1 left an open door — “a constraint-based WHO that is not INTAKE-DRY and not a C1–S2B transfer.” Slate-3 only closed the MCL-fade well.
- **Delta:** the door is empty **estate-wide**, not just on MCL fade. Previously unscreened envelope cells (Grains, Livestock, EUREX rates, FVS) die on standing laws *before* they become a WHO. The four census backlog items are now screened as WHO-candidates (still not seeds).
- **Frequency:** second consecutive zero-WHO pass (slate-3 → this track). Not a yield fire (four G0s this week; pre-G0 deaths remain two).

**Inherited bars (not re-derived):**

1. Req 1a four clauses ([ADR 2026-07-26 §2-A](../../adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md)): constraint not preference; WHEN before data; WHY = capacity/awkwardness; HOW = constraint observable. Delete/flip still binds. “Stops get hunted” / retail-chase inadmissible.
2. E1: not in the 2026-08-10 INTAKE-DRY set; not a transfer of C1 `pdh-pdl-failed-break-reclaim` / C2 `london-range-failed-extension-fade` / C3 `overnight-range-failed-extension-fade` / S2A `pullback-failure-resumption` / S2B `sweep-failure-filtered-continuation`.
3. Board-lite: no index-futures **continuation entry**; no third MR-at-level rr≈1 card.
4. Fade ≥2 independent events/day is a **fade-program** law ([TNEC L2](../../../lab/analysis/harvest/tnec_l2_sourcing_2026-08-10/SOURCES_LOG.md)); TNEC N-ACT is weekly. Census density still binds fade-shaped drafts.
5. R-REQSCOPE: harvest Req 1b/2 do **not** bind internally-composed MSL candidates; 1a + EM0–EM5 + TNEC still do.
6. Same-group opposing legs are a hedge breach ([envelope §4a](../../../ops/prop_envelope_default.md) / fade spec §4.1a). Calendar/crush/crack as two-legged books fail here.
7. No “complete the matrix” ledgers ([ADR 2026-07-25 §5](../../adr/2026-07-25-instrument-profile-index.md)). Unledgered SI/HG/FGBL/ZC stay unledgered unless a named WHO touches them.
8. Magdon-Ismail B is not calibration. Sprint lane closed. Dense-1m temporal-selectivity **paused**. CapFLOW is **not** a TNEC substitute.

---

## §3 — Candidate mechanisms (informal) — product-group sweep

Every row is a **door**, not a seed. No PnL examined.

### Equity Index — MNQ / MYM / MES / M2K

| Door | Why not NEW |
|---|---|
| Continuation entry | S2B route FAIL; Board-lite bars the family |
| MR-at-level (PDH / overnight / London) | C1 / C3 / C2 transfers |
| 0DTE / pin (census backlog 2) | Fade-to-pin = third MR-at-level; fade-away = index continuation. Both expressions barred. Harvest Tier C graveyard-watch (D5 / H-OD parent) |
| MOC / LETF / session-handoff / vol-target / ETF-AP / COT / Russell | Census F1–F5 · P3-1–P3-3 · P4-1–P4-3 **DEAD** |
| ORB / TNEC CON-3–5 / CapFLOW | ORB parked; dense-1m paused; CapFLOW Cap-spend FALSIFIED 2026-08-14 (Cap held), not a WHO |

Index OHLCV directional-timing **raised bar** still binds any leftover OHLCV timing story.

### Energy — MCL / NG (QM / QG same group)

| Door | Why not NEW |
|---|---|
| TAS / settlement / GSCI-roll | BE3 · SFX-1 · Q-MCLTAS-1 — **INTAKE-DRY** |
| EIA / carry / physical | H-FBEIA-1 · H-FCCARRY-1 · LIT-EIA-PHYS — **INTAKE-DRY** |
| PROPENG | DEAD (transmission) |
| USOIL spike-fader / S2A inverse | INTAKE-DRY / post-hoc of S2A FLIP |
| S2A pullback-failure-resumption | Transfer + explore FALSIFIED (N-ACT) |
| Overnight-range failed-extension | C3-K2 transfer |
| `CONFIG-B-MCL` as the WHO | geometry ≠ mechanism |
| Pipeline nomination cycle | §3.1 — sign not entailed (BE1 / SESSION-HANDOFF) |
| Crack / WTI–Brent / calendar | same-group opposing or spread-shaped; F4 adjacency |
| NG weather / HDD-CDD / seasonality | information or calendar preference, not a mandate; EIA print already FALSIFIED; ~29.6 bp hurdle |

### Metals — MGC / SI / HG / PL / PA

| Door | Why not NEW |
|---|---|
| London-range failed-extension (MGC or SI) | C2 transfer |
| PDH/PDL failed-break | C1 transfer |
| LBMA / gold-fix / event-window | R8 `event-window-reversal` **DEAD**; SI is the same class |
| COMEX FND / registered-vs-eligible warehouse | F4 expiry-roll **BLOCKED-BY-REGISTRY**; ~1/month → N-ACT / fade-density fail |
| LME cancelled-warrant → COMEX HG | §3.2 — LME→COMEX transmission (F1 mode); sign not entailed |
| Lease / GOFO | discontinued / no clock |
| PL / PA | thinner metals; same families; no ledger (matrix forbidden) |

### Currencies — M6A / M6E / 6B / 6J / 6C / 6S (no MJY / M6J)

| Door | Why not NEW |
|---|---|
| WMR / Tokyo / NY **fix** cluster | F3 **DEAD** (cost-law + re-proposal bar: *not a different fix*); P3-4 MULTI-FIX-FX **DEAD** |
| 00-figure order-cluster | M6A-FIGURE-FADE **DEAD** (preference) |
| Session-handoff / Asia-range failed-extension | P3-2 **DEAD** / C2–C3 transfer |
| Month-end / IMM / FX roll | F5 / F4 **BLOCKED-BY-REGISTRY** |
| RBA / macro pre-release | `event-window-reversal` + informed-flow shutoff; density ~8/yr |
| AUD ↔ iron-ore / commodity-beta | correlation preference; inventory-logic transfer |
| FX 10:00 NY **option cut** / pin | §3.3 — constraint does not name sign (BE1); delete residue = figure-fade |
| Carry-timing | H-FCCARRY-1 **INTAKE-DRY** |
| MJY as host | **not Tradeify-legal** (`firm_rules` / [`MJY.md`](../../../ops/instruments/MJY.md)) |

M6A envelope remains NON-EMPTY. Envelope ≠ mechanism. Census authored no M6A entry.

### Grains — ZS / ZL / ZM / ZC / ZW (envelope §4a; **full-size**, not micro)

| Door | Why not NEW |
|---|---|
| USDA WASDE / Crop Progress / Export Sales | §3.4 — EIA-family / `event-window-reversal` transfer; **INTAKE-DRY** adjacency (H-FBEIA · LIT-EIA-PHYS). Census backlog 1 asked for a **micro** |
| FND / warehouse receipts | F4 roll family |
| Crush (ZS vs ZL+ZM) / calendar | same-group opposing (§4.1a) |
| WHY / capacity | these **are** the institutional tickets — clause (iii) fails the micro-residual limb |

No grain ledger. Creating one without a named WHO is the matrix motive ADR 2026-07-25 §5 forbids.

### Livestock — HE / LE / GF

USDA cattle-on-feed / cold-storage = same EIA-family print. Full-size. No ledger. Same kills as grains.

### Interest Rates — FGBL / FGBM / FGBS / FGBX (EUREX; US Treasuries venue-dead)

| Door | Why not NEW |
|---|---|
| Bund / Bobl **auction** hedge-unwind | §3.5 — H-ZNAUC-1 family (SCREEN-FAIL on ZN). F3 precedent: a venue change does not raise per-event δ. Full-size → clause (iii) weak. Density ~weekly |
| ECB / macro window | event-window + informed-flow |
| Quarterly roll | F4 **BLOCKED-BY-REGISTRY** |
| ZB/ZN/ZF/ZT/UB | **venue-dead** at Tradeify |

No FGBL ledger. Matrix forbidden until a WHO exists.

### Volatility — FVS

VIX-class roll / variance-premium. Harvest **VENUE-WALL** on the VIX complex; FVS is hedge-cross-linked to Equity Index (long index + long FVS = offsetting). Not a WHO.

### Census pass-3 backlog (now walked as WHO-candidates)

| # | Backlog item | This track |
|---|---|---|
| 1 | Physical / delivery notices (energy or ags); wanted a micro + ≥2/day | Nominations, FND, warrants, USDA: all die before WHO (sign, F4, EIA-family, or full-size) |
| 2 | Options expiry / pin on **equity index** | Both pin expressions Board-lite-barred; FX cut dies in §3.3 |
| 3 | Basis / calendar that is **not** roll-pressure packaging | Still no discriminating observation the 3FPS/ORC record lacked; two-legged books fail §4.1a |
| 4 | Position-limit accountability | Rare state condition; density / N-ACT fail; which side is public with lag |

---

### §3.1 — Pipeline nomination (MCL / NG) — four clauses, then kill

- **(i) WHO:** shippers who must nominate barrels onto named US pipes by a published cycle clock.
- **(ii) WHEN:** nomination deadlines (exchange-adjacent, calendar-published).
- **(iii) WHY:** asserted micro residual on MCL after the physical book clears.
- **(iv) HOW:** published nomination volumes.

**Kill:** the mandate is to *file a nomination*, not to buy or sell MCL at a signed level. Direction is an inventory model (BE1: constraint carries neither sign nor level). Delete residue = “fade/follow inventory” = LIT-EIA-PHYS / H-FBEIA. Not NEW.

### §3.2 — LME cancelled-warrant → HG — four clauses, then kill

- **(i) WHO:** cancelled-warrant holders taking metal out of LME warehouses.
- **(ii) WHEN:** daily LME warrant report (London morning).
- **(iii) WHY:** asserted COMEX-HG residual below LME ticket size.
- **(iv) HOW:** cancelled-warrant stock.

**Kill:** LME→COMEX is indirect transmission (F1 failure mode). Sign (tightness → long) is a discretionary inventory story, not a flatten-at-clock mandate. No HG ledger. Not NEW.

### §3.3 — FX 10:00 NY option cut (M6A) — four clauses, then kill

- **(i) WHO:** vanilla-option dealers who must be delta-flat at the 10:00 New York cut.
- **(ii) WHEN:** every NY business day, 10:00 NY cut window (declared before data).
- **(iii) WHY:** asserted M6A residual below 6A / spot ticket size. Census standing correction: *capacity smallness is not free* (F3: the same littleness destroyed a ~2 bp fix edge).
- **(iv) HOW:** expiry OI / pin distance.

**Kill:** dealer gamma can be long or short; “toward pin” vs “away from pin” is **not** entailed by the flatten-at-cut rule (SESSION-HANDOFF / BE1). Delete the clock and the residue is M6A-FIGURE-FADE (preference, **DEAD**). F3 re-proposal bar: *not a different fix*. MULTI-FIX-FX already bundled the NY clock. Nearest class `event-window-reversal` is DEAD on the settlement/auction/macro limbs. Not NEW.

### §3.4 — USDA prints on ZC / ZS / ZW — four clauses, then kill

- **(i) WHO:** commercials and funds who must mark inventory / production after a scheduled USDA print.
- **(ii) WHEN:** WASDE (monthly) / Crop Progress (weekly Mon) / Export Sales (weekly Thu).
- **(iii) WHY:** fails — full-size grains **are** the institutional tickets; census backlog 1 required a **micro**.
- **(iv) HOW:** the print itself.

**Kill:** this is the EIA / `event-window-reversal` family on a different calendar (H-FBEIA informed-flow signature; LIT-EIA-PHYS; NG-EIA mechanism-present / edge-absent). INTAKE-DRY adjacency. Monthly WASDE fails N-ACT the way S2A failed it. Not NEW.

### §3.5 — Bund auction hedge-unwind (FGBL) — four clauses, then kill

- **(i) WHO:** primary dealers obligated to take down German Finance Agency auctions and hedge duration into the bund future.
- **(ii) WHEN:** published auction calendar.
- **(iii) WHY:** fails — FGBL is full-size, not a micro residual.
- **(iv) HOW:** auction size / cover / tail.

**Kill:** H-ZNAUC-1 already ran this family on ZN (SCREEN-FAIL, cost-law). F3 standing law: a venue change (US Treasury → EUREX) does not raise per-event δ. Re-proposal bar on H-ZNAUC is *new mechanism evidence*, not a different auction calendar. Not NEW.

---

## §4 — Falsifiable hypothesis

**H:** an estate-wide zero-data walk — every Tradeify product group plus the four census backlog items, applying Req 1a + E1 + Board-lite + delete/flip — either **names** a WHO outside the 2026-08-10 INTAKE-DRY set and outside C1/C2/C3/S2A/S2B, or records **deeper dryness** and authors no card.

**Reject H if:** a slate-4 card is authored anyway; a C1–S2B transfer or INTAKE-DRY family is named as NEW; a grain/FGBL/SI/HG ledger is created without a named WHO; or `CONFIG-B-MCL` is treated as a WHO.
**Accept H if:** no WHO is named and no camp is scaffolded (**this pass**), *or* a WHO is named with all four 1a clauses and an executed rejected-nearest that excludes those sets.
**Ambiguous-hold if:** a door is left unscreened that could still clear 1a. (None left on the envelope list.)

---

## §5 — Forbidden moves (this track)

- Author a slate-4 card / scaffold `msl_s4a_*` / add a `MECHANISMS.md` id without a named WHO.
- Name a transfer of C1/C2/C3/S2A/S2B, or an INTAKE-DRY family, as NEW.
- Treat `CONFIG-B-MCL` or “low-WR / high-rr” geometry as a WHO ([design-box](N-2026-08-13-msl-design-box-rederivation.md) is geometry, not a constraint).
- Create SI / HG / ZC / FGBL ledgers to “complete the matrix.”
- Un-pause dense-1m, reopen the sprint lane, or use CapFLOW as a TNEC substitute.
- Cite FALSIFIED(yield) — it has not fired.
- Recalibrate Magdon-Ismail B.

---

## §6 — Gate

| Verdict | Trigger | This pass |
|---|---|---|
| `RESOLVED` (WHO named) | Four 1a clauses + rejected-nearest excluding INTAKE-DRY and C1–S2B | — |
| `RESOLVED` (STILL DRY) | Sweep complete; no WHO; no card | **fired** |
| `FALSIFIED` | Card authored / transfer named as NEW / matrix ledger | — |
| `AMBIGUOUS-HOLD` | A product-group door left unscreened | — (envelope list walked) |

**Disposition:** E1 HOLD unchanged. Charter stays **RATIFIED**. Phase 3 stays **HOLD (E1)**. Death counter stays **2/3** (functional 3/3). Do **not** scaffold `msl_s4a_*`.

---

## §3-routing / next

**STILL DRY — deeper than slate-3.** Slate-3 closed fade × MCL. This track closed the other product groups and the census backlog as WHO-candidates. The next WHO cannot be found by walking this grid again.

CapFLOW Cap-spend discharged **`FALSIFIED` 2026-08-14** (Cap held; not a TNEC candidate). Magdon-Ismail B undecided. F1 clock **2026-11-08** unchanged.

---

## §10 — Audit hooks

```bash
test ! -d lab/analysis/c1/msl_s3a_mcl_2026-08
test ! -d lab/analysis/c1/msl_s4a_mcl_2026-08
test ! -d lab/analysis/c1/msl_s4a_m6a_2026-08
rg -n "STILL DRY" docs/notes/notice/N-2026-08-14-msl-who-track.md
rg -n "P3.8" docs/briefs/2026-08-12-msl-program-plan.md
rg -n "no slate-4 card until NEW WHO" docs/briefs/closures/MSL-S7-closure-resolved-e1-hold.md
# expect: E1 stop rule still present; this notice does not flip it
```

---

## Verification

```bash
python scripts/check_brief.py docs/notes/notice/N-2026-08-14-msl-who-track.md --type notice
```
