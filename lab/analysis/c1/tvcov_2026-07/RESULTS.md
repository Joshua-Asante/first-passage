**Theme:** c1
**Status:** ACTIVE — TV intraday bar-coverage census (Q-TVCOV-1)
# Q-TVCOV-1 — TV intraday bar-coverage census — RESULTS

**Spawn:** Claude Code, executed 2026-07-13 (canonical leg + TV leg + roll-rule correction, same day) · **Brief:** [`docs/briefs/Q-TVCOV-1-tv-bar-coverage-census.md`](../../../docs/briefs/Q-TVCOV-1-tv-bar-coverage-census.md)
**Return taxonomy:** `DONE_WITH_CONCERNS` — both legs complete. **H (coverage-artifact) is FALSIFIED for 6J and MNQ — the 2022 trade-rate break is real.** MYM lands `AMBIGUOUS` on the pre-registered grid solely because of a **one-day TV-history hole (2020-03-16)**; evidence otherwise favors break-real. Concerns: (1) the audit's own first-pass canonical series (`.c.0`) was a roll-rule artifact and had to be corrected mid-audit — verdicts from the first pass are **withdrawn**; (2) the TV MYM 2020-03-16 hole means the Striker-MYM panel never saw the COVID limit-down day.
**Data:** Databento GLBX.MDP3 (`ohlcv-1h` + `ohlcv-1m`; first pass `MYM.c.0/MNQ.c.0/6J.c.0`, corrected pass `MYM.v.0/MNQ.v.0/6J.v.0`, diagnostics `6JU1/6JZ1` raw) — **$0.0000 billed across all pulls** (account on paid subscription; estimate runs inside every `pull` per the ADR gate). TV leg: BAR EXPORT v0.2 List-of-Trades exports (see §TV leg).

---

## §Verdict (per instrument — §6 binary gate, FINAL)

| Instrument | Strategy leg | §4 disposition | Basis |
|---|---|---|---|
| **6J** | Aegis JPY | **H FALSIFIED — break is real** | Corrected canonical coverage complete (pre-break mean 98.86%, intra ≈100%); TV counts match canonical **exactly (0.0% deviation) on all 5 pre-break months** |
| **MNQ** | Striker NAS100 | **H FALSIFIED — break is real** | Canonical complete (96.35% / 99.04%, intra ≈100%); TV within ±0.1% on all pre-break months. Residual pre→post delta ≈ fully explained by the 16:15-ET halt-slot elimination (§Stage 2 read) |
| **MYM** | Striker DJ30 | **AMBIGUOUS (grid) → operator-accepted BREAK-REAL (2026-07-13)** | 4 of 5 pre-break months match exactly; 2020-03 TV −4.3% = a **single missing day (2020-03-16)** in TV history, not era-wide thinness. Below the limb-(b) bar (needs ≥5% on ≥2 months). Parent call taken (§Operator disposition). |

**The 2026-07-12 seven-year panels retain evidential standing, pre-2022 segments included** (MYM with the one-day caveat below). The earlier same-day 6J `ARTIFACT-CONFIRMED` / "pre-2022 6J NON-EVIDENTIAL" verdict is **WITHDRAWN** — it was an artifact of the audit's own symbol choice, not of the data the backtests ran on (§Roll-rule attribution). Per the brief §4, the *why* of the now-confirmed-real frequency break (regime / strategy-structure interaction) is out of scope here.

### §Operator disposition (2026-07-13)

**MYM parent call: BREAK-REAL, operator-accepted.** The grid disposition stays mechanically AMBIGUOUS (limb-(b) tripped by one month), but the operator adjudicates the 2022 MYM trade-rate break as **real** — the sole grid failure is a single fully-characterized absent TV day (2020-03-16, COVID limit-down), and a finer schema cannot add information. MYM now joins 6J/MNQ at **H FALSIFIED — break real**. **Standing annotation obligation (confirmed, not just recommended):** wherever 2020-Q1 Striker-MYM behavior is analyzed, annotate that TV's MYM 15m history is missing Sun 2020-03-15 18:00 ET → Mon 2020-03-16 17:59 ET (the Striker-MYM panel never saw the limit-down session); if that day is needed TV-side it must come from canonical CME data, not TV (§Recommendations #4). **No panel downgrade** — consumers of the 2026-07-12 exports need no other change.

---

## §Roll-rule attribution (the audit's own artifact, caught and corrected)

The first-pass census used Databento's **calendar-rolled** continuous (`.c.0`). Slot-level diff against the TV leg exposed two artifacts, then contract-level pulls (`6JU1`, `6JZ1`, `6J.v.0` for 2021-09) made the mechanism exact:

1. **6J serial-month artifact (large):** after the Sep quarterly's last trade (2021-09-13), `6JU1` printed **zero** in-window bars while `6JZ1` (Dec) covered **34/34 slots every day** — yet `6J.c.0` showed only 1–10 slots/day. Calendar-rank-0 had rolled to the near-dead front **monthly serial** (CME currency futures list serials), not the volume-lead quarterly. `6J.c.0` 2021-09 = 335 covered slots; `6J.v.0` (volume-rolled) = **734 = TV 6J1! exactly**. All pre-2022 `.c.0` 6J "thinness" — and the +15.26pp pre→post "growth" — was this mapping artifact varying in size, not market structure.
2. **MYM/MNQ roll-Friday artifact (small):** the entire c.0-vs-TV gap in e.g. 2019-09 and 2024-03 (+28 slots each) sits on **one day per month** — the quarterly-expiry Friday (2019-09-20, 2024-03-15), where `.c.0` maps to the dying contract while TV `1!` has rolled. **All 9 frozen months are quarterly-expiry months (Mar/Jun/Sep)**, so the sample design put one roll artifact into every month.

**Adversarial confirmation (instrument_id level):** post-expiry, `6J.c.0` carries iid **3182** — neither `6JU1` (244795) nor `6JZ1` (86183) — i.e. a third instrument, the monthly serial. On the MYM roll Fridays, `.c.0` still carries the pre-roll iid (206109 in 2019 / 573705 in 2024) with full-day volume of just 144 / 1,641 contracts. The skeptic also found the artifacts **systemic**: `6J.c.0` is thin in *all nine* sampled months (335–571 vs 680–782 actual — unusable as a coverage/backtest series), and the MYM/MNQ roll-Friday deficit recurs in every sampled quarterly month.

**Lesson (binding for future counts-based audits):** the continuous-symbology roll rule determines which bars *exist*, not merely price continuity. The brief's §0.5-Q2 "confirm the roll letter" check was dismissed first-pass as moot-for-counts — that dismissal was the error. `.v.0` (volume-rolled) is the TV-`1!`-equivalent series; `.c.0` is not, for any CME product with listed serials or around quarterly rolls. Even `.v.0` is only *near*-equivalent: its volume-roll trigger lagged TV's roll by a full session once (6J, 2023-06-16, 9/34 slots, iid 13265→172852 switched Sunday) — treat single roll-week cells with care in any future exact-match test.

---

## §Stage 1 — annual 1h-bar census, corrected series (`.v.0`)

| Instrument | 2019* | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026* |
|---|---|---|---|---|---|---|---|---|
| MYM.v.0 | 3,452 | 5,887 | 5,923 | 5,903 | 5,893 | 5,920 | 5,880 | 2,923 |
| MNQ.v.0 | 3,452 | 5,913 | 5,923 | 5,903 | 5,893 | 5,920 | 5,880 | 2,923 |
| 6J.v.0 | 3,455 | 5,913 | 5,925 | 5,931 | 5,920 | 5,952 | 5,915 | 2,937 |

*Partial years (range 2019-06-01 → 2026-07-01).* **All three instruments are flat across the 2022 boundary** — including 6J, whose first-pass "ramp" (3,585 → 4,288 → 5,281 on `.c.0`) disappears entirely on the roll-correct series. There is no coarse-feed discontinuity anywhere. The ~2×/2.7× trade-rate jumps in the strategy panels are therefore not bar-availability effects.

---

## §Stage 2 — coverage census, corrected series, with TV side-by-side (COMPLETE)

Canonical: covered 15-min grid slots (≥1 one-minute bar, volume>0, bar-open in slot), weekdays 08:00–16:30 ET, 34 slots/day, holiday-dark days excluded from denominator. TV: 15m bars (volume>0, bar-open in window) from the BAR EXPORT leg — each bar is one slot.

| Month | | MYM v.0 | MYM TV | Δ% | MNQ v.0 | MNQ TV | Δ% | 6J v.0 | 6J TV | Δ% |
|---|---|---|---|---|---|---|---|---|---|---|
| 2019-09 | PRE | 680 | 680 | 0.0 | 680 | 680 | 0.0 | 700 | 700 | 0.0 |
| 2020-03 | PRE | 718 | 687 | **−4.3** | 718 | 719 | +0.1 | 748 | 748 | 0.0 |
| 2020-09 | PRE | 713 | 713 | 0.0 | 713 | 713 | 0.0 | 734 | 734 | 0.0 |
| 2021-03 | PRE | 759 | 759 | 0.0 | 759 | 759 | 0.0 | 782 | 782 | 0.0 |
| 2021-09 | PRE | 734 | 734 | 0.0 | 734 | 734 | 0.0 | 734 | 734 | 0.0 |
| 2022-03 | POST | 782 | 782 | 0.0 | 782 | 782 | 0.0 | 782 | 782 | 0.0 |
| 2023-06 | POST | 734 | 734 | 0.0 | 734 | 734 | 0.0 | 723 | 748 | +3.5 |
| 2024-03 | POST | 680 | 680 | 0.0 | 680 | 680 | 0.0 | 680 | 680 | 0.0 |
| 2025-06 | POST | 700 | 699 | −0.1 | 700 | 700 | 0.0 | 714 | 714 | 0.0 |

Coverage ratios (corrected canonical): MYM 96.35% pre / 99.04% post (Δ +2.69pp, AMBIGUOUS band); MNQ identical; 6J **98.86% pre / 99.16% post (Δ +0.31pp — complete both eras)**. Intra-session density ≈100% everywhere — zero intra-session holes on the corrected series.

**The MYM/MNQ residual delta is session structure, not liquidity** (found by the blind verification recounts, present in BOTH feeds identically): the **16:15 ET grid slot is structurally absent through ~2021-Q2** — the CME equity-index daily maintenance halt (16:15–16:30 ET), eliminated in 2021 — capping pre-break months at 33/34 slots per day. One slot of 34 ≈ 2.9pp, i.e. essentially the entire +2.69pp. 6J never had the halt slot. Net: MYM/MNQ pre-2022 coverage was **complete up to a known exchange-session change**; no liquidity-era deficit remains to explain.

Cell notes: **MYM 2020-03 −4.3%** = 29 of 31 missing slots on a single day, 2020-03-16 (§TV leg). **6J 2023-06 +3.5%** = TV *above* canonical — verification traced it to **2023-06-16 (quad-witching roll Friday), where `6J.v.0` covers only 9/34 slots** while TV `1!` is full: the same roll-mapping artifact class in miniature, on the v.0 side this time; direction cannot support the thin-feed hypothesis. **MYM 2025-06 −0.1%** = one 16:15 slot on the export's final day (export window ends 2025-06-30 20:00 UTC). The 2024-03 dark day in all series = Good Friday 2024-03-29 (full CME closure).

---

## §TV leg — BAR EXPORT v0.2 (replaces the abandoned chart-count procedure)

Manual chart counting failed structurally: TV's chart viewport only scrolls back ~11 months of 15m history on the operator's plan, and the deep-backtesting Strategy Tester report requires ≥1 trade to display anything. The repo's **BAR EXPORT v0.2** tool (Pine strategy encoding each confirmed 15m bar's OHLCV in the order Signal field; List-of-Trades CSV as transport; deep-backtesting-compatible) is the correct instrument — it exports the bars **the TV chart engine actually served to a strategy**, which is precisely the population the brief's limb (b) asks about.

- **Exports (operator, 2026-07-13):** `BAR_EXPORT_v0.2_CBOT_MINI_MYM1!_2026-07-13_5f929.csv`, `BAR_EXPORT_v0.2_CME_MINI_MNQ1!_2026-07-13_86a38.csv`, `BAR_EXPORT_v0.2_CME_6J1!_2026-07-13_99781.csv` — landed under `core/data/tv_exports/cme/` (gitignored; hashes pinned in that dir's `SHA256SUMS`).
- **Parse:** production loader `core/bar_export_loader.py` via `scripts/parse_bar_export.py` (v0.2 path; Entry-price==encoded-close cross-check passed on every row; zero skipped rows) → `core/data/bar_data/{MYM,MNQ,6J}_M15.csv` + `.meta.json` sidecars: **137,029 / 137,188 / 161,751 bars**. Epoch field is bar-open **UTC** (authoritative; the CSV Date-and-time column is chart-TZ and ignored).
- **Ranges:** all three start 2019-09-01 (TV's 15m history floor for these roots). MYM/MNQ exports end 2025-06-30 / 2025-07-01; 6J ends 2026-07-01. All 9 frozen months covered by all three.
- **Defect found (real, ~24h):** TV's MYM 15m history is missing **Sunday 2020-03-15 18:00 ET through Monday 2020-03-16 17:59 ET** — the entire limit-down session (first bar back: Mon 18:00 ET) — while canonical CME shows 773 one-minute bars / 113,974 contracts full-day Monday (~99K in-window; canonical itself covered only 29/34 in-window slots that day, consistent with limit halts). MNQ has both sessions. Consequence: any TV MYM backtest — including the 2026-07-12 seven-year Striker-MYM panel — never saw the COVID limit-down day. One session; does not explain the 2020 trade-rate puzzle (20 trades/yr), but worth an annotation wherever 2020-Q1 MYM behavior is analyzed.

---

## §First-pass census (`.c.0`) — SUPERSEDED, retained for audit trail

First-pass numbers (same metric, calendar-rolled series): MYM 92.71%→95.20% (+2.49pp, AMBIGUOUS), MNQ 92.73%→95.20% (+2.47pp, AMBIGUOUS), 6J 57.61%→72.87% (**+15.26pp, ARTIFACT-CONFIRMED**) — that 6J verdict was issued and is now **withdrawn** per §Roll-rule attribution. The first-pass slot diagnostics (6J thin *throughout* the session pre-2022; MYM/MNQ afternoon-slot deficits) were measurements of the wrong contract's liquidity, not of the TV feed. Full first-pass tables reproducible via `census.py <data> "MYM.c.0,MNQ.c.0,6J.c.0"` on the c.0 pulls.

---

## §Confound checks

- **Dataset condition (GLBX.MDP3, 2019-06-01→2026-07-01):** 2,232 `available`, 16 `degraded`, 0 missing/pending; **none of the 16 degraded days intersect any frozen sample month.** Canonical data for every sample-month day was complete-as-served.
- **Zero-volume bars:** 0 in-window across all months/series (ohlcv bars are trade-derived).
- **Verification pass (adversarial, multi-agent):** two independent **blind** recomputes — the TV table from the raw BAR EXPORT CSVs and the corrected canonical table from the parquets, neither agent shown this file's numbers — **matched all 27 cells each (54/54)**. Their sanity sweeps: 0 duplicate epochs, 0 off-grid timestamps (every epoch ≡ 0 mod 900,000 ms), 0 undecodable rows, 0 zero-volume in-window bars; every deficit vs the weekday×34 maximum traced to a named cause (16:15 halt slot, Labor Day / Juneteenth early closes, Good Friday closure, COVID circuit-breaker days, the MYM 2020-03-16 hole). A third, skeptic agent tasked to refute the four attribution claims returned **4/4 CONFIRMED**: (1) v.0≡TV 2021-09 slot-sets exactly identical (symmetric difference 0); (2) c.0 serial-month mapping proven at instrument_id level (iid 3182 ≠ 6JZ1's 86183); (3) roll-Friday concentration exact (per-day diff 0 everywhere except the expiry Friday, both months); (4) MYM hole confirmed and enlarged to ~24h (Sun 2020-03-15 evening included).

---

## §Falsifier disposition (§4, FINAL)

| Instrument | limb (a) canonical thin ≥5pp | limb (b) TV ≥5% below canonical, ≥2 pre months | ±1% match all pre months | Disposition |
|---|---|---|---|---|
| 6J | NOT MET (+0.31pp corrected) | NOT MET (0.0% dev, all 5) | **MET** | **H FALSIFIED — break real** |
| MNQ | NOT MET (+2.69pp) | NOT MET (max +0.1%) | MET (≤0.1%) | **H FALSIFIED — break real** |
| MYM | NOT MET (+2.69pp) | NOT MET (one month, −4.3%) | NOT MET (2020-03) | **AMBIGUOUS (grid) → operator-accepted BREAK-REAL 2026-07-13** — single-day hole; parent call taken (§Operator disposition). Standing 2020-03-16 annotation obligation; a finer schema cannot add information (the deficit is one absent TV day, fully characterized) |

Pre-2022 panel segments **retain evidential standing** for all three instruments (MYM: annotate 2020-03-16). Consumers of the 2026-07-12 exports (account-boundary ADR §0 evidence panels, stage-8 companion §1, 08-08 packet) need no downgrade annotations from this audit.

---

## §Caveats

1. **The corrected canonical series is `.v.0`** (volume-rolled = TV-`1!`-equivalent). Any future count-based comparison must match roll rules first — see §Roll-rule attribution lesson.
2. **Early closes** are era-balanced and intra-density-insensitive (unchanged from first pass).
3. **Frozen months are all quarterly-expiry months** — a design confound discovered here, neutralized by using `.v.0`; future month-freezes should mix expiry and non-expiry months.
4. **TV leg export windows** differ slightly per symbol (MYM/MNQ end 2025-06/07); immaterial to the 9 frozen months.
5. The 6J TV leg is the **full-size** contract (6J1!), matching the exported Aegis panel; the live lane's M6J (micro) is thinner and was not measured here.

---

## §Reproduction

Research venv (`.venv-research`, databento 0.81.0); `DATABENTO_API_KEY` in env; account on paid subscription (bar pulls priced $0). From repo root:

```bash
PY=.venv-research/Scripts/python.exe
DB=lab/databento_fetch/db_fetch.py

# Corrected canonical (volume-rolled) — Stage 1 + one Stage-2 month shown; repeat for all 9
$PY $DB pull --symbols MYM.v.0,MNQ.v.0,6J.v.0 --stype continuous --schema ohlcv-1h --start 2019-06-01 --end 2026-07-01 --max-cost 5.0 --out <data>/stage1_ohlcv1h.parquet
$PY $DB pull --symbols MYM.v.0,MNQ.v.0,6J.v.0 --stype continuous --schema ohlcv-1m --start 2019-09-01 --end 2019-10-01 --max-cost 5.0 --out <data>/stage2_1m_2019-09.parquet

# Census (corrected series)
$PY lab/analysis/tvcov_2026-07/census.py <data> "MYM.v.0,MNQ.v.0,6J.v.0"

# Roll-attribution diagnostics (2021-09)
$PY $DB pull --symbols 6JU1,6JZ1 --stype raw_symbol --schema ohlcv-1m --start 2021-09-01 --end 2021-10-01 --max-cost 5.0 --out <data>/diag_6J_raw.parquet
$PY $DB pull --symbols 6J.v.0 --stype continuous --schema ohlcv-1m --start 2021-09-01 --end 2021-10-01 --max-cost 5.0 --out <data>/diag_6J_v0.parquet

# TV leg (from the landed BAR EXPORT v0.2 CSVs; vendor bytes gitignored, hash-pinned)
python scripts/parse_bar_export.py --symbol MYM --in "core/data/tv_exports/cme/BAR_EXPORT_v0.2_CBOT_MINI_MYM1!_2026-07-13_5f929.csv"
python scripts/parse_bar_export.py --symbol MNQ --in "core/data/tv_exports/cme/BAR_EXPORT_v0.2_CME_MINI_MNQ1!_2026-07-13_86a38.csv"
python scripts/parse_bar_export.py --symbol 6J  --in "core/data/tv_exports/cme/BAR_EXPORT_v0.2_CME_6J1!_2026-07-13_99781.csv"
# TV counts: bars from core/data/bar_data/<SYM>_M15.csv, bar-open UTC→ET, Mon–Fri, [08:00,16:30) ET, volume>0, per month
```

First-pass `.c.0` pulls remain in the DBN cache (`~/.databento_cache/`; keys in the session log) for audit-trail reproduction.

---

## §Recommendations — BAR EXPORT as the standing TV-side instrument

1. **BAR EXPORT v0.2 is now the default TV-side leg for any data-integrity or parity question** — it exports the exact bar population TV serves to strategies (the load-bearing population), sidesteps viewport scroll limits and the tester's needs-a-trade wall, and lands through an existing production parser with a built-in format-drift detector. Chart-counting procedures should not be specified in future briefs.
2. **The landed 2019-09→2026-07 MYM/MNQ/6J 15m bar sets** (`core/data/bar_data/`, hash-pinned) are reusable: TV-vs-canonical parity checks for the futures-prop program, session/coverage studies, and as the TV-side anchor whenever a Databento-sourced result needs a "did TV see the same bars?" cross-check. Refresh cadence: re-export only when a question needs post-2026-07 bars (append pages; the loader dedupes on bar-open time).
3. **Roll-rule pin:** for TV-`1!` comparisons use Databento `.v.0`, never `.c.0`. Candidate one-liner for `databento-data`'s `reference/schemas-and-symbology.md`.
4. **MYM 2020-03-16 hole:** annotate wherever 2020-Q1 Striker-MYM behavior is analyzed; if a future study needs that day on the TV side, it must come from canonical data, not TV.
