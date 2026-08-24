# Notice — Lane B2.0 cost/venue arithmetic (London-fix wake, FX futures)

**Notice ID:** N-2026-08-24-b2-london-fix-wake-cost-arithmetic
**Observed:** 2026-08-24
**Author:** claude.ai (subagent, operator-GO'd this session for Phase B lanes B1/B2)
**Source:** [`docs/superpowers/plans/2026-08-23-viable-strategy-phase-b-mechanism-supply.md`](../../superpowers/plans/2026-08-23-viable-strategy-phase-b-mechanism-supply.md) §Lane B2, task **B2.0 only**
**Status:** `AWAITING OPERATOR BAR-READING` (not GRADUATE/DROP/HOLD — B2.1 is a named, non-self-clearing operator ruling; see §4)
**Lives in:** `docs/notes/notice/N-2026-08-24-b2-london-fix-wake-cost-arithmetic.md`

**Scope discipline:** this note executes **B2.0 only**. It does not rule on B2.1 (the operator
bar-reading) and does not touch B2.2 (placebo battery — gated on both B2.0 *and* B2.1 passing).

---

## §0 — Source anchor (Rule 0)

- **`core/firm_rules.py`** @ `65dc17b` (last commit touching the file, 2026-08-23) — read in full for
  the `Tradeify_Select_100K` block (L367–380) and every FX-adjacent commission comment (L76–101
  Bulenox; L258–265 Tradeify Currencies note). Confirmed via `grep -n "M6E|M6A|cost_per_side_usd"`
  across the whole file.
- **`docs/rejected_candidates.md`** @ `d6b35dd` (2026-08-23) — read the full "FX intraday
  fixing-reversal (session mean-reversion) on EURUSD" entry, L282–300.
- **`git show pre-prune-2026-08-08:docs/notes/notice/N-2026-07-26-forced-flow-census.md`** — read
  the full F3 section (WMR 4pm-London fix flow / M6E), L115–150, plus its own self-audit (L189–222).
- **`ops/instruments/M6A.md`, `M6B.md`, `MJY.md`** (current worktree, all `2026-08-1x` last-touched)
  — read in full; both independently attest "Tradeify Currencies Product Group lists
  6E/M6E/6B/6J/6A/M6A/6C/6S" and "live Tradeify Currencies micro set is M6A+M6E only."
- **Tradeify Help Center, live primary source, fetched 2026-08-24** (browser, not WebFetch — the
  domain 403s a bare fetch):
  - [`Rules: Supported Trading Products / Assets`](https://help.tradeify.co/en/articles/10468222-rules-supported-trading-products-assets)
    (page dated "May 20, 2026" — matches the article number `10468222` already cited in
    `firm_rules.py` L291–296).
  - [`Trading Commission Fees`](https://help.tradeify.co/en/articles/10468315-trading-commission-fees)
    (page dated "April 28, 2026" — matches article `10468315` already cited in `firm_rules.py`
    L261–265).
- No `ops/instruments/6E.md`, `6B.md`, or `M6E.md` exists in the worktree (`Glob ops/instruments/*.md`,
  confirmed fresh this session) — matches the task brief's claim.

---

## §1 — What B2.0 asked, and what firm_rules.py actually contains

**Finding 1 — `cost_per_side_usd` is a single flat scalar per firm/tier, never per-instrument.**
`Tradeify_Select_100K`'s `cost_per_side_usd` field (L378) is `0.91` — documented in its own comment
as "all-in, index micros (MNQ/MYM/MES; MGC=$1.06)." Grepped the entire file for any per-instrument
override structure (`cost_per_side_usd\[`, `COST_OVERRIDE`, etc.) — **none exists**. Several closed
`lab/archive/` studies *do* reference M6A/M6E (`dl2_m6a_pdhpdl_2026-08-22`,
`tnec_envelope_compile_2026-08`, `transfer_expression_grid_2026-08`, `six_lead_cf_2026-08-17`) — the
default Grep tool sweep missed these (`.rgignore` excludes `lab/archive/`, per
`lesson_rgignore_excludes_archive_from_repo_research`; a plain `grep -rl` from Bash catches them).
Read one (`tnec_envelope_compile_2026-08/instruments.py` L4–6, L72–74): it derives M6A's
`tick_value` from the third-leg map's own connecting arithmetic — `RT 1t $2.82 = 2×$0.91 + tick`
— i.e. it **also** used the flat generic `$0.91` field, not M6E/M6A's true `$0.80`/side FX rate.
No file anywhere in the repo (live code or archived study) reads a coded M6E/M6A-specific cost
constant; every consumer either uses the flat `0.91` field or transcribes the Stage-1 table that
itself used that flat field. The true Tradeify M6E/M6A commission ($1.60 round-trip, per L262
comment, sourced to the same article `10468315` verified live above) is **comment-only** — never
coded into a field any engine reads. Confirms the brief's suspicion.

**Finding 2 — full-size 6E/6B are legal at Tradeify, but wholly unmodeled in `firm_rules.py`.**
Live-verified 2026-08-24 (`Rules: Supported Trading Products / Assets`): the "Currency Futures"
table lists **6A, 6B, 6J, 6C, 6S, 6E** — all six full-size FX majors, CME-listed, no exclusion
noted. The "MICRO Futures" table lists only **M6A** and **M6E** — no M6B, no MJY/M6J. This
independently reproduces (does not just trust) `M6A.md`/`M6B.md`'s in-repo attestation. **`6E` and
`6B` never appear anywhere in `firm_rules.py`, in a comment or a field** (grepped `"6E"|"6B"|M6B`
across the whole file — zero hits beyond the Bulenox M6A/M6B/M6E micro-rate comment). No cost,
no margin, no cap row exists for them. The task brief's premise is correct: this is genuinely
unpriced venue surface, not an oversight in a table I overlooked.

**Finding 3 — live commission figures, fetched 2026-08-24 (`Trading Commission Fees`, free-plan
schedule, same schedule `firm_rules.py`'s `0.91` figure is drawn from):**

| Symbol | Round-trip commission | Source |
|---|---|---|
| M6E (micro) | **$1.60** | matches `firm_rules.py` L262 comment exactly |
| M6A (micro) | **$1.60** | matches `firm_rules.py` L262 comment exactly |
| 6E (full-size) | **$6.20** | new — not in `firm_rules.py` |
| 6B (full-size) | **$6.20** | new — not in `firm_rules.py` |

CME contract facts (web-verified 2026-08-24, standard published specs, cross-checked against two
independent sources each):

| Symbol | Contract | Tick size | Tick value | Pips/tick |
|---|---|---|---|---|
| M6E | €12,500 | 0.0001 | **$1.25** | 1 tick = 1 pip |
| 6E | €125,000 | 0.00005 | **$6.25** | 1 tick = **½ pip** ($12.50/pip) |
| 6B | £62,500 | 0.0001 | **$6.25** | 1 tick = 1 pip |

---

## §2 — The 4× cost-floor arithmetic (two conventions, both run)

Two round-trip-cost conventions appear side by side in this repo's own prior work and give
materially different answers, so both are shown rather than silently picking one:

- **"1-tick-total"** — matches the third-leg instrument map's own `RT 1t` column (e.g. its `MES`
  row: `$1.82 commission + $1.25 = $3.07`, reproduced exactly) and roughly reproduces Lane B1.0's
  own "~2.3 ES-points" anchor (this convention gives 2.46 pts for MES — same ballpark).
- **"1-tick/side"** — F3's own literal formula for M6E: `RT = 2($0.80) + 2($1.25) = $4.10`. This is
  the more conservative convention and is F3's own precedent, so it is the fairer one to hold this
  lane to for direct comparability.

`hurdle_$ = 4 × RT_$`; `hurdle_pips = hurdle_$ / pip_value_$`.

| Expression | RT (1-tick-total) | Hurdle (1-tick-total) | RT (1-tick/side) | Hurdle (1-tick/side) |
|---|---|---|---|---|
| **M6E (micro)** | $2.85 | **9.12 pips** | $4.10 | **13.12 pips** |
| **6E (full-size)** | $12.45 | **3.98 pips** | $18.70 | **5.98 pips** |
| **6B (full-size)** | $12.45 | **7.97 pips** | $18.70 | **11.97 pips** |

**Confirms:** M6E micro fails as expected — 9.1–13.1 pips required against the brief's own cited
~3–8 pip literature drift range, worse under either convention. `firm_rules.py`'s M6E third-leg
Stage-1 screen (`c1_thirdleg_instrument_map_2026-07-27/RESULTS.md`) independently marks M6E
`E-COST` — consistent, though that closed study used the flat `$0.91` generic field rather than
M6E's true `$0.80`/side rate, so its own number is not reused here.

**Corrects the brief's "~2.6 pips, full-size 6E/6B" anchor — 6E and 6B are NOT arithmetically
equivalent, and neither figure recomputes to ~2.6:**
- **6E** comes out **3.98–5.98 pips** — inside or at the edge of the ~3–8 pip literature range, i.e.
  genuinely "not an obvious fail," but not the comfortable clearance "~2.6, feasible" implied.
- **6B** comes out **7.97–11.97 pips** — at or above the top of the literature range under either
  convention, and under the conservative (1-tick/side, F3-matching) convention its hurdle (**11.97
  pips**) is essentially the same magnitude as micro M6E's (**13.12 pips**) — 6B is not a materially
  better expression than the micro leg the brief expected to fail. The reason: 6B's tick is a full
  pip ($6.25), half of 6E's per-pip value ($12.50), so the same dollar cost translates to roughly
  double the required pip move.

**DD-fit (confirmed, brief's anchor holds):** a 4–8 pip stop = $50–$100/contract on 6E, $25–$50 on
6B — both trivially inside the $3,000 `Tradeify_Select_100K` trail (`max_dd_pct: 3.0`, L370) under
either convention; not a binding constraint at either expression.

**Cap headroom (light note, not binding):** `micro_contract_cap: 80` (L377, "8 mini / 80 micro,"
account-aggregate per L248–254) extends to full-size legs at the same 10-micro-equivalent-per-mini
counting rule — up to 8 full-size 6E/6B contracts combined with any other book leg. Not a
constraint at any plausible B2 candidate size.

**Hedging note (light, not currently triggered):** 6E and 6B share Tradeify's Currencies Product
Group; the hedging rule (opposing directions within a group prohibited, L277–287) would only bind
a two-leg opposite-direction FX book, which B2 as described (single-direction fade) does not
propose.

---

## §3 — Frozen kill criterion check

Plan's own text: *"B2.0 arithmetic fail at every legal expression → dead."*

Full-size **6E** is not an arithmetic fail under either convention run above (3.98–5.98 pips sits
inside/at-the-edge of the brief's own ~3–8 pip literature-drift range). Since at least one legal
expression does not fail, **the frozen kill criterion does not mechanically fire.** This note
therefore does **not** touch `docs/rejected_candidates.md`, `STATE.md`, or `docs/SESSIONS.md` — no
registry row is warranted, per the task's own instruction that a registry write requires the kill
criterion to fire with zero judgment left.

---

## §4 — Routing: not GRADUATE/DROP/HOLD — a named operator bar-reading (B2.1)

This is deliberately **not** a self-cleared routing decision. Task B2.1 is named in the parent plan
as *"operator bar-reading (named, not self-cleared)"* and this note's own mandate forbids offering a
recommendation on it. What follows is the comparison for the operator to weigh — evidence only.

### F3's exact kill text and re-proposal bar (from primary source, quoted in full)

> **Kill 1 — the mechanism family is already rejected.**
> [`rejected_candidates.md`] §"FX intraday fixing-reversal (session mean-reversion) on EURUSD"
> (rejected 2026-06-22, class: venue/cost-constraint): the daily London 16:00 WM/Reuters fix
> microstructure (Krohn-Mueller-Whelan, *J. Finance* 2024) was cost-pre-screened on the canonical
> Pepperstone 5m EURUSD panel, n=1,550 fix-days. Gross reproduced the paper (~2 bp, best cell
> +0.0455R, correct-signed) and still died: best-of-grid break-even 0.277 pip ≪ ~0.8 pip all-in
> retail. Its re-proposal bar is explicit: *"materially better-than-retail execution evidence OR a
> genuinely different mechanism — NOT a re-tune of the hold/stop grid, a different fix, or a wider
> panel."* ... A futures expression of the same fix is a venue change, which the bar admits only
> if execution is materially better. It is not:
>
> **Kill 2 — M6E makes the cost geometry ~4× WORSE, not better.** [...] That is 11.8× over
> break-even (the rejected CFD was 2.9× over).

(`git show pre-prune-2026-08-08:docs/notes/notice/N-2026-07-26-forced-flow-census.md`, F3 section,
verbatim except for the elided M6E arithmetic already reproduced in §2 above.)

Registry's own re-proposal bar (`docs/rejected_candidates.md` L289, verbatim): *"evidence of
materially better-than-retail execution on the fix (the paper survives only at half-spread), OR a
genuinely different mechanism. NOT a re-tune of the hold/stop grid, a different fix (Tokyo/
Frankfurt), or a wider panel — the cost geometry, not the parameters, is what failed; re-tuning is
the named degeneration move."*

### This lane's own distinct WHO/window (from the parent plan, verbatim)

> Lane B2 mechanism: benchmark-mandated fix flow (10:58–11:04 ET cluster) creates dealer inventory
> whose normalization is faded **11:10–13:00 ET** — sign read from the mechanically-defined
> fix-window impulse.

This is explicitly **not** the fix-print event itself (10:58–11:04 ET) that F3/the registry entry
scored — it is a claimed later, calmer wake window in which dealer inventory built during the fix
is said to unwind. F3's own registry entry and the closed cost-screen study
(`lab/archive/fixrev_costscreen_2026-06-22/`) both score **entry at/into the 16:00 London fix
print**, not a post-fix dealer-normalization window on a different clock (10:58–13:00 ET vs 16:00
London / 11:00 ET-ish NY-equivalent — note the plan's own WHEN is a **different fix cluster time**
than F3's "London 16:00" language; whether this is the *same* WM/Reuters fix read on a different
session convention, or a genuinely distinct fix event, is itself unresolved by this note and is
part of what the operator is being asked to weigh).

### The question for the operator (B2.1, verbatim from the parent plan)

*"Does the wake-WHO clear F3's 'not a different fix' re-proposal bar as new mechanism evidence?"*

**Evidence for "yes, new mechanism":**
- The WHO is dealer-inventory normalization (a distinct causal claim from "the fix print itself
  moves the exchange rate"), scored in a distinct clock window (11:10–13:00 ET) that does not
  overlap the fix print (10:58–11:04 ET) F3 scored.
- F3's own measured 0.277-pip break-even was produced by a specific hold/stop grid search **at
  the fix event itself**; this lane's window is 2+ hours later and structurally could carry
  different (unmeasured) volatility/liquidity characteristics — plausibly calmer execution
  conditions than the fix-print moment the "frozen 1-tick/side" slippage convention above was
  calibrated against, though this is not measured by this note.
- Full-size 6E's cost floor (3.98–5.98 pips) is a materially different cost geometry than the
  micro M6E figure ($4.10, 3.28 pips RT) F3's Kill 2 scored — F3's "makes the cost geometry ~4×
  worse" finding was specific to the micro expression only; F3 never scored full-size 6E/6B.

**Evidence for "no, still the same fix, re-tuned":**
- The underlying flow being faded is still the same WM/Reuters-mandated benchmark fix — the
  re-proposal bar's own wording explicitly excludes "a different fix" (Tokyo/Frankfurt) as a
  qualifying difference; a different *time offset from the same fix* reads, on its face, as closer
  to "a re-tune of the hold/stop grid" (the bar's other named exclusion) than to "a genuinely
  different mechanism."
- No independent literature or measured cohort δ is cited for the 11:10–13:00 ET wake window
  specifically — F3's own 0.277-pip break-even is the only measured number in this estate for any
  expression of this fix family, and it was measured on cash EURUSD at the fix print, not on this
  window.
- The registry's own sibling caution (`rejected_candidates.md`, adjacent custodian-family
  month-end-flow entry) treats "different clock, same mandated flow" as within the same mechanism
  family, not a new one.

This note takes no position between these two readings. **Disposition: LIVE-AWAITING-BAR-READING.**

---

## Verification

```bash
# Tradeify_Select_100K cost/DD/cap fields (confirms §1/§2 figures)
$ sed -n '367,380p' core/firm_rules.py

# Confirms cost_per_side_usd is a single flat scalar, never per-instrument
$ grep -n "cost_per_side_usd" core/firm_rules.py

# Confirms M6E/M6A commission is comment-only, never a coded field, and 6E/6B never appear
$ grep -n "M6E\|M6A" core/firm_rules.py
$ grep -n '"6E"\|"6B"\|M6B' core/firm_rules.py   # zero hits outside the Bulenox M6A/M6B/M6E comment

# Confirms no consumer reads an M6E-specific cost field (note: the Grep tool's default
# .rgignore excludes lab/archive/ -- use plain grep/Bash for a true negative claim)
$ grep -rl "M6E\|M6A" --include=*.py .
$ sed -n '1,8p;70,75p' lab/archive/tnec_envelope_compile_2026-08/instruments.py

# Confirms F3's kill text and re-proposal bar verbatim
$ git show pre-prune-2026-08-08:docs/notes/notice/N-2026-07-26-forced-flow-census.md | sed -n '115,151p'
$ sed -n '282,300p' docs/rejected_candidates.md

# Confirms no ops/instruments ledger exists yet for 6E/6B/M6E
$ ls ops/instruments/ | grep -iE '^(6e|6b|m6e)\.md$'   # expect: no output
```
