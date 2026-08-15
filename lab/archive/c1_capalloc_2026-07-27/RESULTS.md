# Q-CAPALLOC-1 — RESULTS

> ⚠ **The headline run below is SUPERSEDED — read the Addenda (2026-07-28 / 07-29 / 07-29b) first.**
> The original harness inherited the eval-lock defect and ran at pins later verified wrong; the
> re-run at verified pins killed `48/32` and produced **`51/29`** (verdict stays `AMBIGUOUS (d)`,
> conversion is an operator call). Do not quote the pre-addendum split. Body unedited (Trap #12);
> this banner is the reader-intercept (operational_rules.md Rule 14).

**Verdict: `AMBIGUOUS (d)` — a dominating split exists under the modeled rules, but its
dominance does not survive the unverified venue pins. No live change.**

**Pre-registration (FROZEN, unrun at signature):**
[`Q-CAPALLOC-1-verdict-preregistration.md`](lab/archive/../../docs/briefs/pre-registration/Q-CAPALLOC-1-verdict-preregistration.md)
@ `4fac99c` · **Runner:** [`run_capalloc.py`](run_capalloc.py) @ `62be057` (landed unrun)
· **Raw:** [`measured.json`](measured.json) · **Log:** [`run.log`](run.log)
**Ran:** 2026-07-27 · 12 cells × {full, H1, H2} × 3 seeds (11/12/13) × 6,000 paths × 2,600 bd,
plus the §6(d) sensitivity pass. Rung fixed at the ratified WATCH-1 **0.50×**.

---

## §1 — Controls (all five green; §6 row c is the load-bearing one)

| # | Control | Result |
|---|---|---|
| 1 | Incumbent reproduction vs the 2026-07-27 session | eval median **12.2 mo** (want 12.2) · first payout **5.5 mo** (want 5.5) · `E[cash]` **$32,903.8** (want $32,904.0, 1sd tol $167.5) — **OK** |
| 2 | Live 69/11 vs canonical 68/12 | byte-identical daily series (same reserve pair (8,1)) |
| 3 | Candidate set | reproduces the frozen §5 twelve cells, in order |
| 4 | Compliance invariant (D5) | every cell's max combined stack ≤ 80 micros |
| 5 | Half-panel coverage | H1 778 bd (2020-08-04→2023-07-27) + H2 778 bd (2023-07-28→2026-07-21) = 1,556 |

Control 1 is what licenses the runner's one performance refactor. `build_day_index` hoists the
block draw out of the per-cell loop on the argument that `run_scenario` re-seeds per scenario, so
every cell draws identical `picks`; reproducing the incumbent's three published figures to
$0.2 on cash and 0.0 mo on both medians **proves** the equivalence rather than asserting it.

---

## §2 — Measured (median months; `E[cash]` mean over the funded horizon)

| cell | res MYM/MNQ | full-panel net | H1 eval | H1 pay | H1 cash | H2 eval | H2 pay | H2 cash |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 15/65 | 1/5 | $91,840 | 15.7 | 6.9 | $21,922 | 11.9 | 5.1 | $44,176 |
| 9/71 | 1/6 | $95,682 | 15.0 | 6.5 | $23,584 | 11.8 | 5.1 | $44,088 |
| **17/63** | 2/5 | **$95,907** | 14.7 | 6.5 | $24,817 | 11.0 | 4.8 | $47,333 |
| 26/54 | 3/4 | $91,678 | 13.9 | 6.1 | $27,355 | 10.1 | 4.2 | $52,943 |
| 37/43 | 4/3 | $82,145 | 12.5 | 6.3 | $29,932 | 9.1 | 4.2 | $56,653 |
| 34/46 | 4/4 | $95,745 | 12.3 | 5.9 | $29,575 | 9.4 | 3.9 | $55,034 |
| **48/32** | 5/2 | $65,024 | 12.6 | 6.9 | $31,299 | 8.3 | 4.0 | $54,505 |
| 43/37 | 5/3 | $85,917 | 11.3 | 6.0 | $31,643 | 8.5 | 4.0 | $57,549 |
| 59/21 | 6/1 | $47,370 | 16.4 | 8.0 | $27,757 | 9.3 | 4.2 | $44,510 |
| 51/29 | 6/2 | $69,090 | 12.3 | 6.9 | $31,739 | 7.9 | 3.8 | $53,777 |
| 60/20 | 7/1 | $51,141 | 16.8 | 8.0 | $26,818 | 9.0 | 4.2 | $42,587 |
| **68/12** | **8/1** | $55,206 | **17.3** | **7.9** | **$25,585** | **8.9** | **4.1** | **$40,487** |

Last row is the **incumbent** (live 69/11). Every non-incumbent cell reaches its first payout
faster than the incumbent on H1 — the incumbent is the *slowest* cell in the chop half.

---

## §3 — Gate application (§4 D1–D5, both halves independently)

**Only `48/32` (reserve 5/2) satisfies D1–D5 on both halves**, and it does so under **both**
readings of the seed-noise floor (D1/D2-only, and all-four) — so the §4 under-specification
recorded in §6 below is **moot on these data**, not load-bearing.

| cell | H1 D1–D5 | H2 D1–D5 | binding failure |
|---|---|---|---|
| 17/63 (sweep argmax) | D1 ✓ D2 ✗ **D3 ✗ D4 ✗** | **D1 ✗** | H1 pass −15.17 pp, dead@1y +17.49 pp; **slower than incumbent on H2** (−2.73 mo) |
| 34/46 | D1 ✓ D2 ✓ **D3 ✗ D4 ✗** | **D1 ✗** (−0.25 mo) | H1 pass −11.24 pp, dead@1y +15.25 pp |
| 43/37 | D1 ✓ D2 ✓ **D3 ✗ D4 ✗** | all ✓ | H1 pass −5.79 pp, dead@1y −9.86 pp |
| **48/32** | **all ✓** | **all ✓** | — (H1 headroom thin: D3 +2.32 pp, D4 +1.11 pp) |
| 51/29 | D1 ✓ D2 ✓ D3 ✓ **D4 ✗** | all ✓ | H1 dead@1y −1.08 pp |

### The load-bearing finding: the full-panel argmax is regime-fragile

`17/63` has the **highest full-panel net ($95,907, +74% over the incumbent)** and was the
argmax of the disclosed 69-cell sweep. It **fails the gate decisively** — 15–17 pp worse on
both H1 survival axes, and *slower to first payout than the incumbent* on H2.

Shifting cap toward MNQ buys P&L and sells chop-half survival, monotonically. Pooled net
cannot see that trade; the halves price it. This is
`lesson_full_panel_masks_regime_split` reproducing exactly, and it is why §5 forbade the
argmax and §4 gated on both halves rather than the (burned) pooled panel.

---

## §4 — Why the verdict is AMBIGUOUS, not RESOLVED

§6 row (d) fires. `48/32`'s dominance **does not survive the three unverified rule pins**:

| Sensitivity arm | Winners |
|---|---|
| base (`WIN_MIN` $200 · `CAP_LO` 40 · `PAYOUT_MIN` $1,000) | `48/32` |
| **`WIN_MIN` = $100** | **(none)** |
| **`WIN_MIN` = $300** | **(none)** |
| **`CAP_LO` = 80** (no reduced funded start tier) | **(none)** |
| `PAYOUT_MIN` = $500 | `48/32`, `51/29` |
| `PAYOUT_MIN` = $2,000 | `48/32` |

Three of five arms flip the verdict to no-winner. The fragile pins are **the $200 winning-day
minimum** and **the 40-micro funded start tier** — both flagged ⚠ secondary-sourced in the
book-composition brief §0 and **never confirmed in-dashboard**. `PAYOUT_MIN` is not fragile.

The whole result therefore rests on two venue facts nobody has verified against Tradeify's own
dashboard. That is precisely the contingency §6(d) was written to catch.

---

## §5 — Disposition (mechanical, per §6)

1. **No `LEG_MAP` change.** The incumbent 69/11 stands unchanged. Nothing in this run authorizes
   a live sizing edit, and the B7 sequencing in §8 is untouched.
2. **The Tradeify rule-pin dashboard verification is now a HARD BLOCKER**, not a background
   obligation — [`2026-07-24-tradeify-rulepin-verification.md`](lab/archive/../../docs/notes/2026-07-24-tradeify-rulepin-verification.md).
   It was already on the operator queue for the book-comp D1 SHIP path; this run makes it the
   gating input for a second, independent decision.
3. **On pin verification, re-run this harness unchanged** (`python lab/archive/c1_capalloc_2026-07-27/run_capalloc.py`)
   with the confirmed values substituted in `gap_stage2_capbound.py` L32–34. If `48/32` survives
   at the *verified* pins, the verdict converts to `RESOLVED-INCUMBENT-DOMINATED` and routes to an
   amending ADR + operator GO, still sequenced after B7. **This is a re-run at corrected inputs,
   not a new look** — no fresh K, candidate set and gate unchanged.
4. **Recorded for the operator, claimed by nothing here:** the incumbent is the slowest cell in
   the chop half (H1 first payout 25.2 months vs 19.5 for `48/32`), and the 2026-07-22
   re-allocation's P&L cost remains unpriced in the GO ADR.

---

## §6 — Under-specifications in the frozen §4, resolved in the open

Neither is an amendment (Trap #12); both were resolved *before* results were seen and are
disclosed here rather than chosen silently.

1. **Which sd the seed-noise floor compares against** was not pinned. The runner takes
   `max(candidate, incumbent)` — conservative for a gate built to resist false positives.
2. **"Every margin" vs non-inferiority.** D3/D4 are guards, not improvement claims; applying an
   improvement floor to them risks making the gate unreachable by construction
   (`lesson_gate_reachability_preregistration`). The runner scored **both** readings.
   **They agree on these data** (`48/32` under both), so the ambiguity is moot here and no
   §6(b) AMBIGUOUS trigger fires on this axis.

The §6(d) sensitivity **brackets** ({100, 300} / {80} / {500, 2000}) are likewise the runner's
disclosure — the frozen text names the pins but not their alternative values.

---

## §7 — Honesty limits

- **The pooled panel is burned** (§7 of the pre-registration, K_looked = 69 + 2). Full-panel
  figures appear in `measured.json` as diagnostics and were given no power to accept or reject.
- **A both-halves PASS establishes dominance robust across two regimes; it does not establish
  optimality**, and cannot rule out that the reserve-plateau structure is an artifact of this
  panel's composition. The forward check is realized per-leg fills after B7, not another re-run.
- **`48/32`'s H1 margins are thin** (D3 +2.32 pp, D4 +1.11 pp). Even at verified pins this is a
  narrow pass, not a comfortable one.
- **Sizing here is modeled from panel qty**, not from live fills. Q-COSTGEO-3's finding that the
  MYM add is ~13× median displayed depth is unmodelled in every cell, and cuts *toward* smaller
  MYM reserves — reported, and deliberately not scored (§5 forbidden moves).


## Addendum 2026-07-28 — inherited eval-lock defect (blocks the owed re-run as-is)

`run_capalloc.py:179` calls `G.eval_sim` from
[`../tradeify_book_composition_2026-07-23/gap_stage2_capbound.py`](lab/analysis/tradeify_book_composition_2026-07-23/gap_stage2_capbound.py),
whose `eval_sim` applies the **Funded-Flex-only** floor lock (freeze at $100,100 once EOD
peak ≥ $103,100) **during the evaluation**. Tradeify evaluations have no drawdown locking
(article 10495897). Direction is **optimistic**: the lock engages below the $106,000 target,
so every passing path crosses it, and at the target the modeled floor sits $2,900 below the
true one (≈97% of the whole $3,000 allowance).

**What this touches here:** every cell routed through `eval_sim` — the eval pass/median
inputs to the chain rate, hence the `AMBIGUOUS (d)` disposition and the `48/32`
dominating-split finding (whose H1 margins were already thin at +2.32 / +1.11 pp).

**Consequence for the owed re-run** (STATE.md operator queue, item 4 dependent (b)): the
re-run is currently specified as "re-run the harness **unchanged** once the three ⚠ pins are
dashboard-verified." **That is no longer correct** — running it unchanged reproduces the
defect and would bank a contaminated result as a decision. The lock must be scoped to
`funded_sim` first (`eval_sim`: `floor = peak - DD` unconditionally); the pin verification
and the lock fix are independent and both required.

Full record: [`docs/briefs/2026-07-23-tradeify-book-composition.md`](lab/archive/../docs/briefs/2026-07-23-tradeify-book-composition.md)
§Addendum 2026-07-28. Frozen pre-registration cited above stays byte-unedited (Trap #12).


## Addendum 2026-07-29 — pins verified: two of three are WRONG, and one is unmodellable by flag

The three rule pins this study's `AMBIGUOUS (d)` verdict hangs on were verified against the
published Tradeify help-centre article
([Select Flex and Select Daily Payout Policies](https://help.tradeify.co/en/articles/12853966-select-flex-and-select-daily-payout-policies),
read 2026-07-29). **1 of 3 matched.** No login was needed — these are program-wide rules, so the
"blocker is a dashboard login" framing was wrong; what was missing was a read.

| Pin | Modeled | Verified | Match |
|---|---|---|---|
| `WIN_MIN` (100K winning-day min) | $200 | **$200** | **Y** |
| `CAP_LO` (funded start tier) | 40 micro | **30 micro**, scaling 30→40→50→80 | **N** |
| `PAYOUT_MIN` (Flex minimum payout) | $1,000 | **no minimum exists for Flex** | **N** |

**Consequence for this study's disposition.** §6(d)'s sensitivity grid tested
`CAP_LO ∈ {40, 80}` and `PAYOUT_MIN ∈ {500, 1000, 2000}`. The **true values (30 and 0) sit outside
both brackets**, so:

- the "$1,000 payout minimum is not fragile" finding **never covered the actual value**; and
- the funded start tier's **true** value was never tested in any arm.

`48/32`'s dominance is therefore **neither confirmed nor refuted** by the sensitivity work already
done — it is untested at the verified pins. The verdict stays `AMBIGUOUS (d)`; nothing here
converts it.

**The re-run is no longer "the harness unchanged."** Disposition item 3 above says to re-run this
harness unchanged once pins are verified. That is **superseded**: the real scaling rule is
four-step and EOD-calibrated, while `funded_sim` models a single binary step
(`cap = where(tier_hi, CAP_HI, CAP_LO)`). `--cap-lo 30` would model 30→80 and skip the 40 and 50
rungs — a differently-wrong number, not a corrected one. The re-run is gated on the harness change
spec'd in
[`docs/superpowers/specs/2026-07-29-funded-contract-scaling-4step-design.md`](lab/archive/../docs/superpowers/specs/2026-07-29-funded-contract-scaling-4step-design.md),
**plus** the already-merged `eval_sim` lock fix (PR #544).

Confirmed correct and unchanged: `TIER_UNLOCK = 103,000` (the final rung) and `CAP_EVAL = 80`
(evaluations are explicitly *not* scaled). Record:
[`docs/notes/2026-07-24-tradeify-rulepin-verification.md`](lab/archive/../docs/notes/2026-07-24-tradeify-rulepin-verification.md).


## Addendum 2026-07-29b — re-run executed at the verified pins; `48/32` is dead, `51/29` emerges, verdict stays `AMBIGUOUS (d)`

Run pair executed 2026-07-29 after the four-step funded ladder landed
(`docs/superpowers/specs/2026-07-29-funded-contract-scaling-4step-design.md`).

**Drift check (legacy arm, `--funded-ladder legacy --payout-min 1000`): PASSED.**
All three incumbent control pins reproduce — `eval_med_mo` 10.3/10.3, `first_pay_mo` 5.5/5.5,
`mean_cash` 32,903.8 vs 32,904.0. **The harness is sound**; every difference below is a rule
change, not drift.

### The winner set moved twice, and the first move was NOT the funded correction

| Configuration | Winners |
|---|---|
| 2026-07-27 run of record (defective eval + modeled funded) | `48/32` |
| legacy arm (**corrected eval** + modeled funded) | **(none)** |
| verified arm (corrected eval + **verified funded**) | **`51/29`** |

**The eval-lock fix alone destroyed `48/32`'s dominance** — before any funded-pin correction was
applied. That is a materially different attribution than "the funded pins killed it": at modeled
funded pins with a corrected eval, *no* split clears the floor. The funded corrections then
surfaced a different winner, `51/29` (6 MYM / 2 MNQ contract shape), on **both** floor definitions.

`48/32` is not a winner under any corrected-eval configuration tested. Its 2026-07-27 standing is
**superseded**, not merely caveated.

### Verified-arm verdict

```
VERDICT: AMBIGUOUS (d) — verdict flips under unverified rule pin(s): WIN_MIN=100, PAYOUT_MIN=2000
```

Sensitivity at the verified pins: `51/29` **holds** under `FUNDED_LADDER=legacy` and
`PAYOUT_MIN=500`; it **flips to no-winner** under `WIN_MIN=100` and `PAYOUT_MIN=2000`.

### The (d) clause's premise is now stale — an operator decision, not a self-authorized conversion

Row (d) fires on flips under **"unverified rule pin(s)"**. As of 2026-07-29 **all three pins are
verified** (`WIN_MIN` $200 confirmed; `FUNDED_LADDER` corrected to the four-rung ladder;
`PAYOUT_MIN` confirmed to be **none**). The two flipping alternatives — `WIN_MIN=100` and
`PAYOUT_MIN=2000` — are therefore counterfactuals about values now **known to be false**, not live
uncertainty. On its own wording the clause no longer has a subject.

**This addendum does not convert the verdict.** Reading a frozen gate's clause as inapplicable, and
banking the RESOLVED it unblocks, is a §6 interpretation change and belongs to the operator
(Trap #12). The mechanical verdict stands as **`AMBIGUOUS (d)`**.

**Substantive caveat that survives either reading:** `51/29`'s margin is *not* comfortable. It
does not survive a halving of the winning-day threshold or a doubling of a payout minimum that does
not exist. Tradeify rules drift (the verification note carries a standing 90-day re-verify duty),
so a split whose dominance depends on the current values of two verified-but-mutable pins is a thin
result, not a robust one.

### Standing dispositions

- Q-CAPALLOC-1 remains **`AMBIGUOUS`**; no live sizing change; the rail stays disarmed.
- This was a **re-run, not a new look** — no fresh K; candidate set and gate unchanged (§5/§6).
- Control 1 is now **pins-conditional** with a fail-closed drift sentinel (see the run_capalloc
  header comment); the override path refuses to emit a verdict without a passing paired legacy run,
  proven by an adversarial negative test.

## Addendum 2026-07-30 — Q-CAPALLOC-2 executed: verdict `RESOLVED-FRAGILE`

**Successor pre-registration:**
[`Q-CAPALLOC-2-verdict-preregistration.md`](lab/archive/../../docs/briefs/pre-registration/Q-CAPALLOC-2-verdict-preregistration.md)
(§9 operator-signed `509193b`, 2026-07-30, **before** any drift cell ran — Trap #12 ordering
verified: `git log` on the pre-reg file predates every cell artifact's timestamp). Full detail:
[`capalloc2/RESULTS.md`](capalloc2/RESULTS.md); raw per-cell artifacts in
[`capalloc2/`](capalloc2/).

### What Q-CAPALLOC-2 asked

Does `51/29` — the split that clears D1–D5 on both halves at the verified pins
(`WIN_MIN=200, PAYOUT_MIN=0`) per the addendum above — retain that dominance across the six
drift cells a realistic Tradeify re-tier could produce (`WIN_MIN` ∈ {150, 200, 250} ×
`PAYOUT_MIN` ∈ {0, 250}, 3×2 fully crossed, frozen before any cell ran)?

### Controls

Legacy drift sentinel (`--funded-ladder legacy --payout-min 1000`) **PASSED**: eval 10.3 / pay
5.5 / cash 32,903.8 vs pins 10.3 / 5.5 / 32,904.0 — reproduces the 2026-07-29 re-run's drift
control to $0.20, so every difference across the six cells below is a rule-pin change, not
harness noise.

### The 6-cell grid

| cell | `WIN_MIN` | `PAYOUT_MIN` | `51/29` both halves, strict floor |
|---|---:|---:|:---|
| `w150_p0` | 150 | 0 | **FAIL** — H1 clears the raw D4 threshold (headroom +0.07 pp) but fails the seed-noise floor (`d4_headroom_pp < max(candidate_sd, incumbent_sd)`); harness's own embedded verdict for this cell is `AMBIGUOUS (b)` |
| **`w200_p0`** (verified) | **200** | **0** | **PASS** — H1 D1 +5.22 mo / D2 +32.5%; H2 D1 +0.91 mo / D2 +34.8% (matches the 2026-07-29 re-run reference exactly) |
| `w250_p0` | 250 | 0 | PASS |
| **`w150_p250`** | **150** | **250** | **FAIL** — H1 D4 headroom **−0.60 pp** (dead@1y 25.75% vs incumbent 23.15%), a literal breach, not a noise-floor call |
| `w200_p250` | 200 | 250 | PASS |
| `w250_p250` | 250 | 250 | PASS |

Intersection across all 6 cells: **empty**. Verified centre cell: **clears**. Per §6, this is
exactly the `RESOLVED-FRAGILE` trigger (clears at the verified cell, fails ≥1 drift cell) —
disqualifies `RESOLVED-ROBUST` and is not `FALSIFIED` (which would require failing the verified
cell itself). `w150_p250` is the corner the pre-reg's §7 pre-declared expectation named as the
genuinely uncertain, informative cell before any cell ran; it is also the binding failure.

**Verification performed before accepting this table:** re-ran `capalloc2/score_grid.py`
independently against the six raw `w*.json` artifacts (not the summary RESULTS.md) and it
reproduces `RESOLVED-FRAGILE, failing_cells=['w150_p0', 'w150_p250']` exactly. Read `score()` in
`run_capalloc.py` directly to confirm the D3/D4 "strict" floor literally applies
`headroom >= max(candidate_sd, incumbent_sd)` — the seed-noise floor is not a post-hoc gloss on
`w150_p0`, it is the harness's own coded criterion, inherited unchanged from the parent. **One
tooling wrinkle, not a computation defect:** `capalloc2/grid_fast.log` (the parallel runner used
for the three `PAYOUT_MIN=250` cells) logs `FAIL`/blank exit codes for all three jobs — a
PowerShell `Start-Process`/`Wait-Process` exit-code-capture quirk, not a run failure. All three
JSON artifacts are present, parse cleanly, and reproduce the scores above; `run_cell_fast.py`
only clears the parent's own unused 5-arm `SENSITIVITY` sweep (confirmed by reading it) and
leaves the D1–D5 `main()` scoring path byte-identical.

### Disposition (per §6 — no operator decision invented here)

Adoption of `51/29` is conditional on rules that may move. Per the frozen gate: route to
operator with the failing cell named, and an explicit re-verify tripwire on `WIN_MIN=150`, **or**
decline. No plain GO is available under this verdict. No `LEG_MAP` edit, no arming, no rung
change made or implied; any live change stays sequenced after B7-REFIRE Stage 2 + its own
amending ADR per §8.5. Q-CAPALLOC-1 remains `AMBIGUOUS (d)`, byte-unedited (Trap #12).

### Operator disposition 2026-07-30 — DECLINED; `69/11` stands; question CLOSED

Operator ruling (chat directive, same day: "Let's go with what the data says", electing the
decline route of §6's FRAGILE row as recommended by the session's data summary). `69/11` stands
as ratified; no `LEG_MAP` change, no amending ADR, no tripwire adoption. Grounds and the three
preconditions bound to any future re-open — (a) D4 re-scored under intraday barrier enforcement
(PR #566), (b) reconciliation against realized post-B7 per-leg fills, (c) pins re-verified within
the standing 90-day window — are recorded in the closure artifact, which is the owner of record:
[`Q-CAPALLOC-2-closure-resolved-fragile.md`](lab/archive/../../docs/briefs/closures/Q-CAPALLOC-2-closure-resolved-fragile.md).
