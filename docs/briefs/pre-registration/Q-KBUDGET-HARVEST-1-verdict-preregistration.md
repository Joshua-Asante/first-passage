# Pre-registration — Q-KBUDGET-HARVEST-1 bounded literature harvest (frozen formula)

**Status:** **FROZEN — operator locked 2026-07-16.** The commit that lands this status is the freeze commit; cite via `git log --format='%h %ci' -- <this file> | tail -1`. No item in §B/§C/§D/§E changes after Phase-1 extraction begins. Extracting a paper before this freeze commit voids that paper's harvest row.
**Parent brief:** [`docs/briefs/Q-KBUDGET-HARVEST-1-bounded-axis-literature-sweep.md`](../Q-KBUDGET-HARVEST-1-bounded-axis-literature-sweep.md)
**Loop of record:** OUTER (inventory expansion; axis-funding remains STRATEGIC-LoR at 2026-08-08)
**Feeds:** 08-08 axis-selection packet (alongside D5); does **not** gate D5 `register_search open`
**Authored:** 2026-07-16 · Cursor Cloud (assembly) · operator-directed lock
**Ratified:** 2026-07-16 · Joshua (operator) — "lock the harvest Pre-Q"

---

## §A — Why freeze before extraction

Q-KBUDGET-1 resolved with a single PASS (D5). Expanding the inventory from literature is cheap (zero pulls, zero K) but selection-shaped: which papers get read, which δ get extracted, and which rows get offered for ratification can drift toward a desired slate if the source list and gate are not frozen first. This file freezes the verdict table, the four-field extraction template, the Tier bars, the seed exclusions, and the enumerable query-family coverage rule **before** Phase 1 opens a paper.

## §B — Verdict gate (verbatim from parent §6; frozen)

| Verdict | Trigger | Disposition |
|---|---|---|
| `RESOLVED` | ≥1 harvested row operator-ratified + `floor_scan.py` extended and run (zero pulls / zero K) | Inventory addendum + extended RESULTS; ranked additions feed 08-08 packet alongside D5 |
| `FALSIFIED` | Frozen Tier-1/Tier-2 coverage rule fully discharged (§E); zero four-field-complete candidate rows emitted | Close empty; 08-08 slate stays D5-only; capture whether the source list was too narrow (lesson candidate) |
| `AMBIGUOUS-HOLD` | Well-formed rows emit but ratification deferred past 2026-08-08 | Name deferred rows; do not extend the harness; reopen only via fresh Pre-Q |

**Pre-registered before Phase-1 extraction.** Amending this table mid-harvest is Trap-12 → close AMBIGUOUS and reopen fresh.

## §C — Extraction template (frozen §C four admission requirements)

Every candidate row **must** carry all four:

1. **Instrument family** → `K_banked` (from closed manifests; else 0)
2. **Search-design class + coarse tool ladder** → `K_intrinsic` (mechanism-first ≤3 preferred; wide-mining / locked-K designs are recordable FAIL-invariants)
3. **OOS era + expected event rate** → `N` (declared panel event count)
4. **Cohort-cited effect prior δ, σ** → Clause N **or** explicit `UNSCREENABLE` naming the missing input

Inherited Clause-K/N formulas: parent screen pre-reg [`Q-KBUDGET-1-screen-preregistration.md`](Q-KBUDGET-1-screen-preregistration.md) §B (freeze `b304f2c`) — not re-derived here.

## §C.1 — Economic-grounding pre-check (amendment, 2026-07-16, pre-Phase-1)

**Additive, not a rewrite of §C's four fields** — landed before Phase 1 began (§A ordering preserved; `ls lab/analysis/harvest/q_kbudget_harvest_1_2026-07/` confirmed empty at amendment time, per §F hook #4). [`docs/adr/2026-07-15-external-mechanism-harvest-intake.md`](../../adr/2026-07-15-external-mechanism-harvest-intake.md) (`Accepted` same day) is the standing front-door doctrine this bounded sweep now executes under. Its requirement 1 is a mandatory pre-check, applied **before** a row is logged against the §C four-field template:

A candidate clears economic grounding via **either**:
- **Path 1a** — named mechanism (who systematically loses money and why).
- **Path 1b** — evidence-robustness in lieu of a settled mechanism, for anomalies with no consensus mechanism (the momentum-class shape Q1/Q2/Q6 are likely to surface): **all four** of (i) ≥3 decades covered sample period; (ii) ≥3 independent non-overlapping cohorts; (iii) ≥1 replication published ≥10yr after original discovery; (iv) no known sign-reversal condition (name any found — do not assert immunity).

A candidate clearing neither path is `EXCLUDE:no-economic-grounding` in the Phase-1 coverage log — logged with the reason, never silently dropped, same discipline as any other exclusion. This does not relax or replace any of the original four fields (K_banked / K_intrinsic / N / δ,σ); it gates entry into them.

## §D — Tier bars (frozen)

| Tier | Admission bar |
|---|---|
| **Tier 1** | Peer-reviewed journal; **per-instrument or per-index futures** cohort with extractable central δ/σ (or β/t/R² convertible **without** cross-instrument transplant) |
| **Tier 2** | Reputable working paper or handbook/survey chapter with the same extractable per-instrument δ/σ bar |

**Out of scope (frozen exclusions):** vendor marketing decks; SPX-only γ-sign estimates transplanted to NQ/YM; blogs; anything requiring a paid dataset pull to *obtain the δ* (procurement is a different Pre-Q); reopening DISC-CAMP-0 or Q-HARV-1 as harvest candidates (calibration citations only).

## §E — Source-list appendix (frozen at lock)

### E.1 — Seed sources already in-repo (must be logged in Phase 1; disposition fixed)

| Seed | Tier | Disposition at lock |
|---|---|---|
| Baltussen, Da, Lammers & Martens 2021, *JFE*, "Hedging demand and market intraday momentum" (NQ/YM cohorts) | 1 | **Already inventoried as D5** — do not re-emit as a "new" axis. Sibling constructs from the *same paper* only if they declare a **distinct** family/design/N/δ 4-tuple (else skip). |
| Amaya, Garcia-Ares, Pearson & Vasquez 2025 (gamma-sign; SPX cohort) | 1 | **Examined/excluded** — no NDX/Dow cohort; SPX→NQ/YM transplant forbidden (parent §5 / D5 rescreen). Log as covered. |
| Q-HARV-0 / Q-HARV-1 month-end ES cohort (+13–19.2 bp) | in-house | **Already inventoried as D3** (FAIL N) — calibration only; do not reopen. |
| HARV class-analogue used for D7 | in-house | **Already inventoried as D7** (FAIL N) — calibration only. |

### E.2 — Query families Phase 1 must cover (enumerable coverage rule)

Phase 1 runs a documented search pass for **each** family below (Scholar / SSRN / journal sites as available). For each family, log: query string(s) used, date, sources examined (title + venue + year), and four-field outcome (`ROW` / `EXCLUDE:<reason>` / `UNSCREENABLE:<missing>`).

| # | Query family (mechanism / design class) | Target families (preferred) |
|---|---|---|
| Q1 | Intraday momentum / hedging-demand / dealer-hedging **price footprint** (not γ-sign) | NQ/MNQ, ES, YM (YM only if liquidity caveat recorded) |
| Q2 | Session-timing / opening-range / last-hour futures anomalies with **per-contract** stats | NQ, ES, YM, GC |
| Q3 | Order-flow or inventory-hedging footprints with per-index **futures** cohorts | NQ, ES |
| Q4 | FX-futures microstructure timing (6E / 6J) with extractable δ | 6E, 6J (note M6J absent at FRIENDLY firms) |
| Q5 | Metals mechanism-first (not mining) with extractable δ — record K_banked=3,177 FAIL-invariant honestly if prop expression requires GC/MGC | GC/MGC (likely FAIL K; still log) |
| Q6 | Tier-2 anomaly surveys / handbooks reporting **instrument-level** futures δ or net Sharpe (not SPX-only) | any unbanked or low-K family |

**Coverage discharge (feeds §B FALSIFIED):** all six query families have a dated coverage log entry in `lab/analysis/harvest/q_kbudget_harvest_1_2026-07/` **and** the union of logged sources yields zero four-field-complete *new* candidate rows (seed dispositions in E.1 do not count as new rows).

**Not frozen here:** the specific paper titles Phase 1 will discover under Q1–Q6 — those are the harvest product. Freezing invented titles would be confabulation; freezing the query families + coverage rule is the load-bearing lock.

## §F — Audit hooks (runnable)

```bash
# 1. Freeze commit is this file's first FROZEN landing
git log --format='%h %ci %s' -- docs/briefs/pre-registration/Q-KBUDGET-HARVEST-1-verdict-preregistration.md | tail -5

# 2. Parent brief locked (not still DRAFT)
grep -n 'Status.*OPEN' docs/briefs/Q-KBUDGET-HARVEST-1-bounded-axis-literature-sweep.md | head -3
grep 'DRAFT (pre-lock)' docs/briefs/Q-KBUDGET-HARVEST-1-bounded-axis-literature-sweep.md && echo "STILL DRAFT — fail" || echo "lock OK"

# 3. Parent Q-KBUDGET-1 still RESOLVED (harvest does not reopen)
python3 lab/archive/q_kbudget_1_2026-07/floor_scan.py | tail -3

# 4. No Phase-1 artifacts before freeze (ordering)
ls lab/analysis/harvest/q_kbudget_harvest_1_2026-07/ 2>/dev/null && echo "REVIEW: harvest dir exists — check freeze ordering" || echo "clean (pre-Phase-1)"

# 5. No K consumed
grep -rn "Q-KBUDGET-HARVEST\|KBUDGET.HARVEST" discovery_manifests/ 2>/dev/null && echo "REVIEW" || echo "no harvest manifest (expected)"

# 6. Economic-grounding pre-check present before any Phase-1 row
grep -n "Path 1a\|Path 1b\|no-economic-grounding" docs/briefs/pre-registration/Q-KBUDGET-HARVEST-1-verdict-preregistration.md
```

## §G — History

| Date | Event | Who |
|---|---|---|
| 2026-07-16 | Parent Pre-Q drafted (`OPEN — DRAFT (pre-lock)`) | Cursor Cloud |
| 2026-07-16 | **FROZEN** — operator lock; §B–§E locked; Phase 1 unblocked | Joshua (operator) |
| 2026-07-16 | §C.1 economic-grounding pre-check added (Path 1a/1b, inherited from ADR 2026-07-15) — landed before Phase 1 began; additive, §B/§C/§D/§E rows unedited | Claude Code (reconciling PR #391 against the harvest-intake ADR, operator-directed) |
