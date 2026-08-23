# Q-TOM-SPX-1 — SPX500 turn-of-month: existence, post-2001 persistence, real-time capturability

**Status:** `CLOSED — DEAD` (Layer-A `RESOLVED-ABSENT` 2026-06-16; reserved Pine unpaid; operator GO 2026-08-23)
**Authored:** 2026-06-15
**Closed:** 2026-08-23
**Authors:** Joshua + claude.ai (advisor) + Claude Code (landing / execution)
**Parent question:** N/A
**Sub-questions opened:** none
**Loop:** Inquire-phase Pre-Q — closure gated on whether a turn-of-month premium **exists, persists (survives the documented post-2001 decay), and is capturable net of real cost** on the **canonical TV/Pepperstone SPX500** feed. (On the Dukascopy exploratory feed the persistence test is realized as post-2011 only — decay UNTESTABLE there; see W4/§9.)
**Artifact path:** `docs/briefs/Q-TOM-SPX-1.md`

> **Scope note (operator decision 2026-06-15):** this brief was **placed, not run**. Q2 = "fix ledger + place artifacts, no Layer-A run until the feed is in hand." It is therefore the pre-registration; the run is a later session. Q1 fixed the feed scope to **persistence-only** (Dukascopy 2011+) for the exploratory cross-check, canonical decay only via the Pine harness on long-history TV.

---

## §0 — Rule 0 reads (production-source verification)

Files read **2026-06-15 before authoring**, worktree HEAD `6268912`:

- `lab/analysis/noct_spx/CARD.md` — anchor `1711155` (2026-06-07). Establishes the **prior SPX500 concept** (NOCT-SPX-001 FALSIFIED) the package's ledger draft denied; the Dukascopy `USA500IDXUSD` data route, `point_factor=1e3`, ~2011 history start, and the "no recorded SPX500 spread" cost gap.
- `docs/rejected_candidates.md` — anchor `88e11dc` (2026-06-14). Confirms the harness-fed rejection `inventory-reversal-immediacy-premium × SPX500` (lines ~123–124) — the collision the draft's check missed.
- `docs/adr/2026-06-12-rnd-feed-instrument-class-split.md` — anchor `034452d` (2026-06-12), **Status: PROPOSED** (ratification gated on Q-FEED-1). **SPX-class indices: TV/Pepperstone canonical; Dukascopy index symbols exploratory-only / never gate-bearing.** The sibling `tv-csv-canonical-feed-policy` (ratified) already makes all bar feeds staging-only, so the conservative posture holds regardless of (this ADR's) ratification. Load-bearing for the whole feed posture.
- `docs/adr/2026-06-12-tv-csv-canonical-feed-policy.md` — anchor `6f8063a` (2026-06-12). General TV-CSV-canonical / bar-feeds-staging policy.
- `core/lib/dukascopy.py` — anchor `a43919b` (2026-06-07). `fetch_candles(..., granularity)` supports `"D"` (daily); index symbols require explicit `point_factor`; closed-hour 503 skip+count.
- `ops/instruments/XAUUSD.md` — anchor `ef5f471` (2026-06-15). Freshest ledger template + the identical web-handoff-confabulation precedent (its session log).
- `docs/adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md` — anchor `2b171fc` (2026-06-12). Instrument-ledger governance (operational rule 10).

**Citation-chain note (gitignored Pine):** the canonical harness `tom_test_spx500.pine` is gitignored (`**/*.pine`) and held locally at `lab/analysis/legacy/tom_spx/`. Its parameters are concept-stage / unvalidated (nothing locked), so no Tier-1 source-constant citation is load-bearing here; the epistemic-status tags inside the script are the governing record.

---

## §1 — Context & motivation

A claude.ai Tech-Advisor concept package (ledger + Python Layer-A harness + Pine harness) for an SPX500 turn-of-month edge landed 2026-06-15. The TOM effect (Ariel 1987 / Lakonishok-Smidt 1988 / McConnell-Xu 2008) and its leading causal mechanism (Etula et al. 2020 "dash for cash" month-end liquidity) are well-documented, as is a post-~2001 US-large-cap **decay**. The concept is the deliberately **source-independent** counterweight to the hawkish-regime thesis (the 2026-06-10..14 audit's source-diversity discriminating test). Standing doctrine bearing on it: instrument-ledger governance (op rule 10), the 2026-06-12 TV-CSV-canonical + index-class-split feed policy, and the strategy-validation test-ordering battery.

---

## §2 — Prior art / lineage

- **`CONCEPT-NOCT-SPX-001` (FALSIFIED 2026-06-07)** — same instrument, **different mechanism** (overnight inventory-reversal, 02:00–05:30 ET intraday) and window. Admissible (not a duplicate) but supplies the SPX500 infra (`point_factor=1e3`, DST map) and a cost-fragility prior (its thin unconditional drift died at ~1.3–2.0 bps). Ledger D1.
- **`lab/analysis/` mechanism-probe lane** (oil_carry / noct_spx / custodian_eurusd F1 precedent) — cheap falsifier gates whether a concept earns a codify→sweep→validate pass.
- **Feed ADRs (2026-06-12)** — index-class split makes Dukascopy SPX exploratory-only; TV/Pepperstone canonical.
- **No prior TOM-on-SPX500 work** exists — genuinely novel mechanism family for this instrument.

---

## §3 — Question (Q-TOM-SPX-1)

**Pre-Q gate test:** the question names a symptom (is there a tradeable edge / is it a decayed-untradeable artifact), not a fix.

**Q-TOM-SPX-1:** Do SPX500 daily returns carry a turn-of-month premium that (a) exists, (b) persists (survives the documented post-2001 decay), and (c) is capturable in real time net of measured cost — or is it a known-decayed / structurally-untradeable artifact (edge living in the look-ahead T+1 day)? (Decay-survival is testable only on long-history TV; the Dukascopy exploratory feed sees post-2011 persistence only — W4/§9.)

---

## §4 — Falsifiable hypothesis (H-TOM)

**H-TOM:** If the post-2011 `[T+1:T+3]` window-day mean daily return exceeds the off-day mean with Welch **t ≥ 2.0** AND survives label-permutation (one-sided p < 0.05), drop-top-k-months (sign preserved), and both chronological halves > 0, AND the real-time-capturable per-trade expectancy (enter close T+1, exit close T+3) is **≥ 4× the measured round-trip cost**, then a tradeable TOM edge is **PRESENT**; if instead the window ≤ off OR perm p ≥ 0.10 OR t < 1.0 OR drop-top-k flips sign, the edge is **ABSENT / decayed**; otherwise **AMBIGUOUS** (underpowered or cost-marginal).

**Reject H-TOM if:** any hard-absent trigger fires (diff ≤ 0 / perm p ≥ 0.10 / t < 1.0 / drop-top-k flips sign).
**Accept H-TOM if:** full existence + persistence (t ≥ 2.0) + capturability (≥ 4× measured cost) on the **canonical TV/Pepperstone** measurement.
**Ambiguous-hold if:** existence met but 1.0 ≤ t < 2.0 (underpowered), OR capturable net > 0 but < 4× hurdle (real-but-marginal), OR existence met on the exploratory Dukascopy feed only (awaiting canonical confirmation).

---

## §5 — Forbidden moves

- **Sweeping the `[T+1:T+3]` window to maximize the diff** — ruled out: the degrees-of-freedom hazard the Pine tooltip flags. The window is mechanism-anchored (Lakonishok-Smidt classic) and confirmed out-of-sample, never optimized in-sample. (strategy-validation §0: selection tests outrank parameter sweeps.)
- **Letting the Dukascopy Layer-A verdict GATE the concept** — forbidden by the 2026-06-12 index-class ADR (Dukascopy SPX is exploratory-only / never gate-bearing). Genuinely tempting: Dukascopy is one command; the canonical Pine/TV path is manual. If that tempts, that is exactly the move the ADR §Forbidden-moves names.
- **Claiming the post-2001 DECAY was tested on the 2011+ Dukascopy feed** — the vacuous-pass trap (fixed in the harness 2026-06-15). Decay is UNTESTED there; assert it only from a long-history TV chart.
- **Stacking other calendar filters (January / turn-of-week / holiday)** — Swinkels-van Vliet 2012: TOM + Halloween subsume them; stacking is overfitting dressed as confirmation.
- **Reporting a capturability PASS on a guessed cost** — W3: no recorded SPX500 spread. No Layer-B gate closes without a broker-measured round-trip cost.
- **Changing any frozen threshold mid-investigation** (`--split-year` / `--window` / perm-alpha / t-cut / hurdle) — trap #12 (`p`-hacking at the methodology layer); voids the verdict. Close AMBIGUOUS and open a fresh brief instead.
- **Outcome-conditional D-tests** (e.g., "drop the worst months, then test if the edge improves") — categorically forbidden; encodes the conclusion. (drop-top-k is the *opposite*: it tests whether the edge SURVIVES removing the best months.)

---

## §6 — Gate criteria (closure verdict)

Pre-registered (frozen in `q_tom_spx_1.py` + this brief, committed before any run). **The gate-bearing measurement is the Pine harness on the canonical long-history TV/Pepperstone SPX500 feed; the Dukascopy Python run is exploratory pre-look only.**

| Verdict | Trigger condition | Disposition |
|---|---|---|
| `RESOLVED — PRESENT & TRADEABLE` | existence (diff>0 ∧ perm p<0.05 ∧ drop-top-k sign-preserved ∧ both halves>0) ∧ persistence (Welch t≥2.0) ∧ capturable expectancy ≥ 4× **measured** round-trip cost, **on canonical TV/Pepperstone** | promote to codify→sweep→validate; broker-confirm DXTrade ticker+contractValue (W2) |
| `RESOLVED — ABSENT / DECAYED` | any hard-absent trigger (diff≤0 / perm p≥0.10 / t<1.0 / drop-top-k flips sign) | close FALSIFIED; auto-append `turn-of-month-premium × SPX500` to `rejected_candidates.md` |
| `RESOLVED — REJECT EXECUTION DESIGN` | Layer-A existence>0 but post-cost capturable expectancy ≤ 0 (edge lives in the untradeable T+1 day) | close; the *edge* is real but this execution design cannot bank it — no Pine lock |
| `AMBIGUOUS — HOLD` | existence met but 1.0≤t<2.0 (underpowered), OR net>0 but <4× hurdle (marginal), OR PRESENT on exploratory Dukascopy only (canonical TV run outstanding) | re-test window: on canonical TV data / on a broker-measured cost; hold, do not build |

Capturability is **PENDING** (never auto-pass) until a measured SPX500 cost exists (W3). Decay is reported **UNTESTED** on any feed whose history starts after the split year (W4) and never contributes a pass.

---

## §7 — Execution plan (run DEFERRED per Q2; this is the plan of record)

- **Phase 0 — Rule-0 reads.** Done (§0).
- **Phase 1 — CANONICAL (gate-bearing).** Load `lab/analysis/legacy/tom_spx/tom_test_spx500.pine` on a **daily TV/Pepperstone (US500) SPX500 chart with maximum history**. Read the diagnostic table (window vs off means; pre/post-2001 decay) + strategy equity (capturable piece). Tune `commission_value`/`slippage` to measured fills (Phase 3) before reading capturability.
- **Phase 2 — EXPLORATORY cross-check (never gate-bearing).** `python lab/analysis/legacy/tom_spx/fetch_daily.py --out core/data/bar_data/USA500IDXUSD_D1.csv --start 2011-09-18 --end <today>` then `python lab/analysis/legacy/tom_spx/q_tom_spx_1.py --series ...`. Persistence-only; decay UNTESTED.
- **Phase 3 — Cost (W3).** Broker-verify FXIFY/DXTrade SPX500 round-trip spread+commission → set `--cost-pct` / Pine commission.
- **Phase 4 — Verdict assertion.** Run the §6 gate against the **canonical** numbers; produce the §9 closure record.

---

## §8 — Verdict pre-registration

The frozen thresholds are immutable in code **and** in this brief, both committed **before** any Layer-A run. They live in two forms in `q_tom_spx_1.py`, both requiring a code edit to change:

- **argparse defaults** (5): `--split-year` 2001, `--window` `1:3`, `--n-perm` 10000, `--hurdle-x` 4.0, `--seed` 42.
- **hardcoded constants in `verdict()`** (2): perm-alpha `0.05` (existence boundary `r["perm_p"] < 0.05`) and t-cut `2.0` (`r["t_post"] >= 2.0`). These are deliberately NOT argparse-overridable — they are the two most selection-critical thresholds, so freezing them in code is a *stronger* freeze than a CLI default.

This brief + the committed harness **are** the pre-registration; a separate `docs/briefs/pre-registration/` file is unnecessary. The §10 audit hook greps for all seven (incl. the two hardcoded boundaries) so any drift is mechanically detectable. Any change to a frozen threshold VOIDS the verdict (§5 / trap #12).

Pre-registration basis: this brief at the commit that places it (predates Phase 1/2 runs by construction — the run is deferred).

---

## §9 — Sanity checks (run-gate — must PASS before any verdict is read)

Step-0-equivalent for a daily series; the ledger's run-gate. None is optional.

1. **Row count + span:** ≥ ~10 years of daily closes for a powered persistence test; canonical TV reaches pre-2001 (decay testable), Dukascopy ~2011+ (persistence-only).
2. **TDOM forward-count census:** every calendar month resets TDOM to 1 and runs ~1..21; no month with TDOM=0 or an implausible max (catches a month-rollover bug). The Pine `newMonth`/`tdom` and the Python `classify()` must agree.
3. **Monotonic, de-duplicated dates** (the loader drops dup-date rows; confirm the count dropped is small).
4. **point_factor sanity:** levels track the S&P 500 (2016≈2020, COVID≈2452, 2026≈7550) — a 1e3 factor error shows as ~1000× off (catches F1 misconfiguration).
5. **Daily-timeframe integrity:** the Pine guard (`timeframe.isdaily`) is green; TDOM counting is invalid intraday.
6. **Feed provenance recorded:** exploratory Dukascopy vs canonical TV tagged in the run record (a Dukascopy number can never be the gate).
7. **Decay-cohort check:** the pre-split n is non-trivial before any decay claim; else decay is UNTESTED (W4), not a pass.

---

## §10 — Audit hooks (runnable)

```bash
# §6 gate logic intact (incl. the decay-untested-is-not-a-pass regression)
python -m pytest lab/analysis/legacy/tom_spx/test_verdict.py -q          # expect 6 passed

# Frozen thresholds unchanged (any drift VOIDS the verdict, §8/§5).
# 5 argparse defaults + 2 hardcoded verdict() constants. EACH line must return a
# hit; a miss = that threshold drifted (M-AHF: grep the stored form, not the mental form).
grep -nE 'default=2001'            lab/analysis/legacy/tom_spx/q_tom_spx_1.py   # --split-year
grep -nE '"1:3"'                   lab/analysis/legacy/tom_spx/q_tom_spx_1.py   # --window
grep -nE 'n-perm.*default=10000'   lab/analysis/legacy/tom_spx/q_tom_spx_1.py   # --n-perm
grep -nE 'hurdle-x.*default=4\.0'  lab/analysis/legacy/tom_spx/q_tom_spx_1.py   # --hurdle-x
grep -nE 'default=42'              lab/analysis/legacy/tom_spx/q_tom_spx_1.py   # --seed
grep -nE 'perm_p"\] < 0\.05'       lab/analysis/legacy/tom_spx/q_tom_spx_1.py   # perm-alpha (hardcoded)
grep -nE 't_post"\] >= 2\.0'       lab/analysis/legacy/tom_spx/q_tom_spx_1.py   # t-cut (hardcoded)

# Collision-guard intact: NOCT-SPX-001 recorded as a prior SPX500 dead concept
grep -n 'NOCT-SPX-001' ops/instruments/SPX500.md                  # expect D1 row
grep -n 'inventory-reversal-immediacy-premium' docs/rejected_candidates.md

# §0 anchors still resolve
git log -1 --format='%h %cs' -- docs/adr/2026-06-12-rnd-feed-instrument-class-split.md

# Decay claim guard: the Dukascopy run must print UNTESTED (never a silent decay pass)
grep -n 'untested-no-pre-data\|DECAY UNTESTED' lab/analysis/legacy/tom_spx/q_tom_spx_1.py
```

---

## Verification

```bash
# Discipline checks (mechanical)
python "C:/Users/joshu/.claude/skills/brief-authoring/scripts/check_brief.py" docs/briefs/Q-TOM-SPX-1.md --type inquire
# Expected: all 6 checks PASS

# Production-source verification (Rule 0 confirmation)
git log -1 --format='%h %cs' -- lab/analysis/noct_spx/CARD.md
git log -1 --format='%h %cs' -- docs/adr/2026-06-12-rnd-feed-instrument-class-split.md

# Cross-reference verification (collision fix landed)
grep -c 'NOCT-SPX-001' ops/instruments/SPX500.md
```

---

## Pre-Lock Checklist (DRAFT briefs only)

- [x] All §0 paths read and anchored with commit hash + date
- [x] §3 question passes the symptom-only rephrase test
- [x] §4 hypothesis is genuinely falsifiable (binary triggers in §6)
- [x] §5 forbidden moves are genuinely tempting, not strawmen (Dukascopy-gating + window-sweep are the live temptations)
- [x] §6 gates have specific numerical triggers
- [x] §8 pre-registration committed BEFORE Phase 1 runs (run deferred by construction)
- [x] §10 audit hooks are runnable commands
- [ ] Verification block executed and passing — `check_brief.py` run pending (below)
