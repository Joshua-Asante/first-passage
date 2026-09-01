# INSTRUMENT LEDGER — MES

**Symbol:** CME Micro E-mini S&P 500 futures (MES; Globex, Databento `GLBX.MDP3`) · **Parent:** [`ES.md`](ES.md) ($50/pt) · **Asset class:** equity index futures
**Status:** **RE-ENTERED — K-void cleared; class-attested; not elected.** Research/discovery only. Third-leg `E-KCAP` elimination voided by [K-bank ADR](../../docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md); standing non-K grounds remain. No live leg, no allocation, no K spend.
**Last updated:** 2026-09-01

**Purpose:** single source of instrument-level truth (operational rule 10, [`docs/adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md`](../../docs/adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md)). Created **2026-08-09** as the live touching session for [`instrument-lane SPEC`](../../docs/spec/2026-08-09-instrument-lane-mcl-mes-mgc-spec.md) — ADR [`2026-07-25`](../../docs/adr/2026-07-25-instrument-profile-index.md) §5. Thin ledger; inherit index class bar from parent ES / sibling [`M2K.md`](M2K.md) M1.

## PROFILE (machine-readable)

```yaml
symbol: MES
asset_class: equity-index-futures
family: [ES]
venue_tradable: true
venue_note: "Tradeify Equity Index Product Group. Withdrawn MNQ/MYM legs no longer reserve cap headroom for new non-Striker research (MSL B8 occupancy release 2026-08-12); Striker redeploy still barred. Correction 2026-08-26: LEG_MAP cap_alloc code WAS edited (both Striker legs' cap_alloc zeroed) — see [Striker LEG_MAP cap-release ADR](../../docs/adr/2026-08-26-striker-legmap-cap-release.md) for current cap_alloc state, not this note."
k_bank_source: "../../discovery_manifests/"
cost_hurdle:
  value: 6.84
  units: "bp"
  basis: "4x MES single-RT hurdle at HARV-2026-001 reference (~4373); parent ES E4"
  source: "../../ops/instruments/ES.md"
bars:
  - id: index-intraday-ohlcv-directional-timing-2026-07-21
    source: "../../docs/rejected_candidates.md"
structure:
  - claim: "Third-leg E-KCAP elimination is void as a gate after K-bank ADR; Clause K no longer eliminates. Standing grounds are Equity Index class bars + S4/S7 occupancy posture, not bank arithmetic."
    source: "#S1"
```

---

## STANDING WARNINGS

- **W1 — Inherit ES roll / continuous warnings.** Parent [`ES.md`](ES.md) W1/W2 (`.c.0` calendar-roll phantoms; UTC-day Sunday bars). MES is the micro sibling — same roll calendar.
- **W2 — Micro-era floor.** MES launched with the index micros (**2019-05-06**). Deep history needs ES parent + proxy discipline; reserve native-micro as OOS.
- **W3 — No Stage-2 σ/τ measured here.** Third-leg N was `—` (never probed). Do not invent Stage-2 cells. Future panel need → databento estimate → operator GO.
- **W4 — Index class bar binds.** [`rejected_candidates.md`](../../docs/rejected_candidates.md) RAISED BAR 2026-07-21 (M2K M1 / ES bars) applies; “new instrument” does not clear it.

---

## DURABLE FINDINGS

| # | Finding | Evidence | Confidence |
|---|---|---|---|
| **S1** | **Voided kill: `E-KCAP`.** Third-leg map eliminated MES as “one seed at cap” (bank 2 → floor 0.98). Banner + [K-bank ADR](../../docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md): Clause K no longer eliminates; bank is disclosure. Current screen floor for `K_intrinsic=1` is 0.650. | [`third-leg RESULTS`](../../lab/analysis/c1/c1_thirdleg_instrument_map_2026-07-27/RESULTS.md) L37 + banner L4–10 | **HIGH** (ADR void). |
| **S2** | **Standing non-K grounds.** Equity Index Product Group · S4 long-only if co-legged · S7 unoccupied symbol vs withdrawn MNQ/MYM (occupancy released for new non-Striker research — [B8 ADR](../../docs/adr/2026-08-12-msl-mym-occupancy-release.md); Striker redeploy still barred) · inherit index OHLCV class bar from ES/M2K · cost-tax from third-leg row (re-cite, don’t re-derive: cost-tax 1t r=1 **0.0982**). | third-leg RESULTS · ES.md · M2K.md M1 · envelope §4a · B8 ADR | **HIGH** as posture; cost-tax is closed-study record. |
| **S3** | **Envelope + TNEC class attestation (no candidate).** See table below. N-SIZE = U (no candidate edge). | this session · [prop envelope](../prop_envelope_default.md) · [TNEC-1](../../docs/spec/2026-08-08-tradeify-necessary-conditions-target-spec.md) | **MODERATE** (class attestation). |

### Envelope E1–E7 + TNEC class attestation

| Limb | Token | Grounds (one line) |
|---|---|---|
| E1 EOD flat | **P** | Micro index; flat-by-16:00 build target inside venue print is design-legal. |
| E2 Consistency | **P** | Soft checkpoint; no instrument-specific kill. |
| E3 Trailing DD | **P** | Intraday trail is firm-parameter; no MES-specific foreclosure. |
| E4 Daily loss | **P** | Present-by-default; size fits inside session stop when a candidate exists. |
| E5 Micro sizing | **P** | MES is the micro unit. |
| E6 Attended automation | **P** | Envelope default; transport-independent bar. |
| E7 News/event | **N/A** | Overlay-only by ratification — default does not constrain. |
| N-SHAPE | **P** (class) | Equity Index · micro-expressible · flat target; **long-only if co-legged** (S4); S7 occupancy vs withdrawn MNQ/MYM — headroom released for new non-Striker research ([B8](../../docs/adr/2026-08-12-msl-mym-occupancy-release.md)); Striker redeploy barred. |
| N-SIZE | **U** | No candidate edge; frontier re-derives per candidate. |

**Dated disposition token:** `RE-ENTERED — K-void cleared; class-attested; not elected`

## DEAD / REJECTED (instrument-specific)

| Rejection | Discriminator | Source |
|---|---|---|
| ~~`E-KCAP` (third-leg)~~ | **VOID as gate** — K-bank ADR; do not inherit | RESULTS banner 2026-08-04+ |
| `closing-auction-moc-wake` | **DROP** — no citable δ, measured expectancy/win rate, or complete expression; B1 source check `STOP`, never started | [`B1 intake closure`](../../docs/notes/2026-09-01-next-vet-intake-decision.md) |

## ACTIVE / OPEN

- Instrument-lane re-screen complete 2026-08-09. Election out of scope.
- Parent ES remains the home for HARV-2026-001 AMBIGUOUS facts; MES inherits cost basis (ES E4) and the index class bar.

## SESSION LOG

- **2026-09-01** — Operator closed both B1 MOC-wake pursuits: strategy `DROP`, source-liveness
  `STOP` before any row. No card/contract/pull/K. Re-proposal bar: independently credible high
  positive net expectancy plus a complete expression; source availability alone does not qualify.
- **2026-08-09** — **Ledger created + K-void re-screen** under [`instrument-lane SPEC`](../../docs/spec/2026-08-09-instrument-lane-mcl-mes-mgc-spec.md). Voided `E-KCAP` vs standing Equity Index / S4 / S7 / class-bar grounds named. Disposition `RE-ENTERED — K-void cleared; class-attested; not elected`. No pull, no K, no election, no `core/` change.
