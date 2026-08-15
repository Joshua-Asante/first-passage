# Q-CAPALLOC-2 — pre-registration: does the dominating cap split survive plausible venue-rule drift?

**Type:** Inquire-phase verdict pre-registration (successor to Q-CAPALLOC-1, which closes `AMBIGUOUS`).
**Status:** `FROZEN` (operator-signed 2026-07-30, §9). Authored 2026-07-29. Nothing in this file has been executed.
**Authors:** Joshua (operator directive: "draft that pre-registration") + Claude Code (Opus 5).
**Parent:** `Q-CAPALLOC-1` (`AMBIGUOUS (d)`, 2026-07-27 / re-run 2026-07-29).
**Why a fresh file rather than an amendment:** Trap #12 — §6 may not be edited after results are seen. Q-CAPALLOC-1 stays closed and byte-unedited; this is the successor it requires.

---

## §0 — Rule-0 reads (verified 2026-07-29)

- [`Q-CAPALLOC-1-verdict-preregistration.md`](Q-CAPALLOC-1-verdict-preregistration.md) — the frozen parent. §4 D1–D5 + seed-noise floor, §5 12-cell enumeration + fixed parameters, §6 verdict table, §7 K accounting. **All inherited verbatim below except the sensitivity brackets.**
- [`lab/archive/c1_capalloc_2026-07-27/RESULTS.md`](../../../lab/archive/c1_capalloc_2026-07-27/RESULTS.md) §Addendum 2026-07-29b — the re-run outcome this successor responds to.
- [`docs/notes/2026-07-24-tradeify-rulepin-verification.md`](../../notes/2026-07-24-tradeify-rulepin-verification.md) — the 2026-07-29 verification: `WIN_MIN` $200 **confirmed**; funded ladder **corrected** to 30→40@$101,500→50@$102,000→80@$103,000; Flex minimum payout **does not exist**.
- `lab/archive/c1_capalloc_2026-07-27/run_capalloc.py` — pins-conditional control + fail-closed drift sentinel; `--funded-ladder` / `--win-min` / `--payout-min`.
- Venue source: [Select Flex and Select Daily Payout Policies](https://help.tradeify.co/en/articles/12853966-select-flex-and-select-daily-payout-policies) — winning-day thresholds **$100 / $150 / $200 / $250** for 25K / 50K / 100K / 150K; Select **Daily** minimum payout **$250**.

---

## §1 — Why this question exists

Q-CAPALLOC-1's §6 row (d) fires when the verdict flips under the three **⚠ unverified** rule pins, and its prescribed remedy is that "the dashboard rule-pin verification becomes a hard blocker on the live change." **That remedy has been executed** (2026-07-29) and all three pins are now verified. On its own wording the clause's trigger no longer has a subject — but converting a frozen gate's verdict on that reading, *after* seeing a favourable result, is precisely the move Trap #12 forbids.

The clause was also pointing at something real that survives its own obsolescence: `51/29` dies under `WIN_MIN=100`. That bracket is a falsified counterfactual, so it cannot gate anything — but Tradeify **does** drift (3.0 in March 2026; consistency moved to real-time; news restrictions removed April 2026; a standing 90-day re-verify duty). The live question is therefore not "does it survive values we now know to be false" but **"does it survive the rule changes this firm actually makes."**

---

## §2 — Prior art / inherited unchanged (zero new researcher DOF)

Everything below is taken verbatim from the parent and **must not be re-derived**:

| Item | Inherited value |
|---|---|
| Candidate set | The frozen **12-cell** structural enumeration (§5 parent). Cell 12 (`68/12` ≡ live `69/11`) is the **control**, never a candidate. |
| Dominance conditions | **D1** first-payout median ≥ 0.50 mo lower · **D2** `E[cash]` ≥ 10% higher · **D3** eval pass ≥ incumbent − 2.0 pp · **D4** dead@1y ≤ incumbent + 2.0 pp · **D5** max stack ≤ 80 micros |
| Seed-noise floor | A margin < 1 sd across seeds on either half **is not a margin** and scores FAIL. |
| Gating partition | **H1 and H2 independently.** Full panel is diagnostic-only and **cannot accept or reject** (burned by the parent's §7 look). |
| Engine | seeds 11/12/13; `n_paths` 6,000; `h_eval = h_fund = 2,600` bd; Mon-anchored week-block bootstrap. |
| Book / rung | c1 2-leg as deployed; **WATCH-1 0.50× only**. Not re-weighted, not re-composed. |
| Drift control | The **fail-closed** pins-conditional control: every override run requires a passing paired legacy-arm sentinel or it emits NO VERDICT. |

**Corrected inputs now in force** (both merged since the parent froze): the `eval_sim` funded-only-lock fix (PR #544) and the four-step funded ladder (PR #546).

---

## §3 — Question (Q-CAPALLOC-2)

**Q-CAPALLOC-2:** Does the dominating cap split identified under verified pins retain D1–D5 dominance on both half-panels across the range of venue-rule values that plausible Tradeify drift would produce?

Symptom-only check: the question names an unmeasured robustness property. It does not presuppose that `51/29` should be adopted, nor that it should not.

---

## §4 — Falsifiable hypothesis (H-CAPALLOC-2; binary)

**H-CAPALLOC-2 — if** at least one candidate satisfies **D1–D5 on both halves at every one of the 6 drift cells**, **then** its dominance is robust to plausible venue drift and routes to an amending ADR + operator GO. **Otherwise** it is drift-fragile and does not.

**Accept H-CAPALLOC-2 if:** ≥1 candidate clears D1–D5 on both halves at **all 6** drift cells.
**Falsifier — H-CAPALLOC-2 is falsified if:** no candidate clears D1–D5 on both halves at the **verified** cell (`WIN_MIN=200, PAYOUT_MIN=0`). In that case `69/11` stands as ratified and the question closes with no live change.
**Partial (fragile) if:** a candidate clears at the verified cell but fails ≥1 drift cell.

Dispositions for each are tabulated in §6.

---

## §5 — The test (FIXED): drift-realistic brackets

The parent's brackets straddled the **modelled** values while the pins were unverified. They are now either falsified (`FUNDED_LADDER` legacy; `PAYOUT_MIN` 500/2000) or counterfactual (`WIN_MIN` 100/300). Replaced with brackets drawn from **how this venue actually changes rules — re-tiering to its own published values**, not arbitrary percentages:

| Pin | Verified value | Drift bracket | Why these values |
|---|---|---|---|
| `WIN_MIN` | **$200** | **{150, 200, 250}** | Tradeify's own adjacent Select tiers (50K = $150, 150K = $250). A re-tier is the realistic drift mode. |
| `PAYOUT_MIN` | **none (0)** | **{0, 250}** | $250 is the minimum Tradeify already applies on Select **Daily** — the realistic value if Flex adopts one. |
| `FUNDED_LADDER` | verified 4-rung | **verified only** | A ladder re-tier is speculative; no published alternative exists to anchor it. **Declared untested** (§7). |

**Grid:** 3 × 2 = **6 cells**, fully crossed. Frozen; no additions after results.

### Why the bracket I first proposed was wrong

My initial suggestion was `WIN_MIN ± 20%` (160/200/240). Reading the parent's results first showed that would have been a **rubber stamp**: `51/29` already survives `WIN_MIN=300` (+50%) and only dies at `100` (−50%), so any ±20% band passes almost by construction. A test that cannot fail is not a test. `$150` is the informative point — **it has never been run**, it is a real published Tradeify value, and it sits between the known-survive and known-die points.

---

### Forbidden moves (each genuinely tempting here)


- **Adding, widening, or dropping a bracket cell after seeing results** — the 6-cell grid is frozen. This is the parent's own failure mode repeating one level up.
- **Reading `RESOLVED-FRAGILE` as `RESOLVED-ROBUST`** because the fragile cell is "unlikely." The bracket exists because the value is *plausible*; discovering it binds is the finding, not an inconvenience.
- **Re-opening Q-CAPALLOC-1's (d) clause** to convert its verdict. It closes `AMBIGUOUS`, byte-unedited; this file supersedes it going forward.
- **Scoring on the full panel.** Burned by the parent's §7 look; halves only.
- **Any live sizing, rung, `LEG_MAP`, or arming change on this file's authority.** A pre-registration authorizes a *run*, never a deployment.
- **Treating the seen centre cell as corroboration.** It is a reference point, not evidence for the drift cells.

---

## §6 — Gate criteria (binary dispositions)

| Verdict | Trigger | Disposition |
|---|---|---|
| **RESOLVED-ROBUST** | ≥1 candidate clears D1–D5 on **both** halves at **all 6** drift cells, every margin ≥ 1 sd | Route to operator + amending ADR for the `LEG_MAP` change. Sequenced **after** B7-REFIRE Stage 2. ADR re-pins `f2_floors.json` and re-runs `pytest tests/ops/ tests/rail_crosstrade/` in the same commit. |
| **RESOLVED-FRAGILE** | Clears at the verified cell (`WIN_MIN=200, PAYOUT_MIN=0`) but fails ≥1 drift cell | **Substantive, not a non-answer.** Adoption is conditional on rules that may move: route to operator with the failing cell named and an explicit re-verify tripwire on that pin, **or** decline. No plain GO. |
| **FALSIFIED** | No candidate clears at the verified cell | `69/11` stands as ratified. Question closes, no live change. Record the measured cost as the price of the 07-22 compliance fix. |
| **AMBIGUOUS** | (a) the fail-closed drift sentinel is unsatisfied, **or** (b) a decisive margin is < 1 sd on either half | (a) run the legacy arm and re-score — no verdict until it passes. (b) report and hold; re-test gated on the first 6 months of live fills, not on a re-run. |

**There is deliberately no "unverified rule pin" ambiguity row.** That clause (parent §6 row d) had its remedy — the dashboard rule-pin verification — executed on 2026-07-29, and all three pins are verified. It is not carried forward.

**Pre-registered before any cell runs.** Amending §4/§5/§6 after seeing results requires closing this pre-registration AMBIGUOUS and opening a fresh one (Trap #12).

---

## §7 — Prior-look disclosure + K accounting (read before scoring)

**This successor is authored with the answer at the centre point already seen.** That is the single largest threat to its validity and is stated plainly:

- Inherited from the parent: `K_looked = 71` (69-cell net sweep + 2 full-panel MC cells).
- **Added 2026-07-29:** the verified re-run was run and read — `51/29` clears D1–D5 on both halves (H1 D1 +5.22 mo / D2 +32.5%; H2 D1 +0.91 mo / D2 +34.8%; margins 9–43× the seed-noise floor), and `48/32` fails under every corrected-eval configuration.

**Why this is still a legitimate test.** The centre cell (`WIN_MIN=200, PAYOUT_MIN=0`) is **not what this question gates on** — it is already known and is carried only as the `RESOLVED-FRAGILE` reference. The gate is the **five drift cells**, and the two informative ones — `WIN_MIN=150` and `PAYOUT_MIN=250` — have **never been run in any configuration**. Seeing the centre does not tell us whether the corner holds.

**No fresh selection K.** The candidate set, D1–D5, and the noise floor are structurally inherited; nothing about *which* candidates are eligible changed. This adds a **robustness axis**, not a selection axis, so no DSR/SPA claim arises and none is made.

**Honesty limit no design here removes.** A both-halves, all-cells PASS establishes dominance robust across two regimes and a plausible drift range. It does **not** establish optimality, and it cannot rule out that the plateau structure is an artifact of this panel. The forward check remains realized per-leg fills after B7 — not another re-run.

---

### Pre-declared expectation (so a surprise is visible)


Recorded **before** running, per the Q-BUSTGATE-1 pattern:

- `PAYOUT_MIN=250` — expected to **hold** (it survives 500, and 250 is nearer the verified 0).
- `WIN_MIN=250` — expected to **hold** (survives 300).
- **`WIN_MIN=150` — genuinely uncertain; this is the cell the question exists for.** It sits between a known-die (100) and a known-survive (200/300), and D1-on-H2 is the binding condition (+0.91 mo against a 0.50 mo threshold — only 1.8× the bar, even at 9σ against noise).
- Overall prior: **`RESOLVED-FRAGILE` is at least as likely as `RESOLVED-ROBUST`.** If the result comes back ROBUST on all six with comfortable margins, that is a *better* outcome than expected and should be treated with corresponding suspicion — re-read the harness before believing it.

**Untested and declared:** funded-ladder drift (no published alternative to anchor a bracket); interaction of drift with the eval phase (both corrections are funded-only); any tier other than 100K.

---

## §8 — Run protocol

1. **Commit this file before any cell runs.** Freeze must precede results (git-auditable).
2. **Legacy drift arm first** — `--funded-ladder legacy --payout-min 1000` — to publish the fail-closed sentinel. A control MISS halts everything; no cell is interpretable without it.
3. Run the **6 drift cells** at the verified ladder; record per-cell winners plus D1–D5 detail and across-seed sd for the incumbent and every candidate.
4. Score §5 against actual numbers. Produce the closure artifact.
5. **Sequencing unchanged from the parent:** any live `LEG_MAP` change is routed **after B7-REFIRE Stage 2**, never before, and the amending ADR must re-pin `f2_floors.json` and re-run `pytest tests/ops/ tests/rail_crosstrade/` in the same commit.

---

## §9 — Authorization (operator directive of record)

```
AUTHORIZED / FROZEN: 2026-07-30 / JA (operator chat directive, this session, verbatim):
"put in §9 and commit"
Scope: measurement only. No LEG_MAP edit, no arming, no rung change, no Pine touch.
```

Signed **before** any drift cell has been run. The centre-cell result disclosed in §7 is the
`RESOLVED-FRAGILE` reference only — not a candidate-set result under this freeze.

---

## §10 — Audit hooks (runnable)

```bash
# 1. Freeze precedes results (the load-bearing discipline claim).
git log --format='%h %cI' -1 -- docs/briefs/pre-registration/Q-CAPALLOC-2-verdict-preregistration.md
git log --format='%h %cI' -1 -- lab/archive/c1_capalloc_2026-07-27/measured.json
#    Expected: this file's commit strictly PRECEDES any Q-CAPALLOC-2 result commit.

# 2. Inherited constants were not silently re-derived (must match the parent verbatim).
rg -n "0.50 months|10%|2.0 pp|80 micros" docs/briefs/pre-registration/Q-CAPALLOC-1-verdict-preregistration.md

# 3. The parent stays byte-unedited after its closure (Trap #12).
git log --oneline -- docs/briefs/pre-registration/Q-CAPALLOC-1-verdict-preregistration.md

# 4. The drift sentinel is gitignored and never committed (fail-closed integrity).
git check-ignore -v lab/archive/c1_capalloc_2026-07-27/_drift_check_legacy.json
git log --all --oneline -- lab/archive/c1_capalloc_2026-07-27/_drift_check_legacy.json   # expect: empty

# 5. The bracket values are the venue's own published tiers, not invented numbers.
#    help.tradeify.co article 12853966: winning-day $100/$150/$200/$250; Daily min payout $250.

# 6. The informative cells were genuinely unrun before this freeze.
rg -n "WIN_MIN=150|PAYOUT_MIN=250" lab/archive/c1_capalloc_2026-07-27/measured.json   # expect: no match
```

---

## Verification

```bash
python ~/.claude/skills/brief-authoring/scripts/check_brief.py \
  docs/briefs/pre-registration/Q-CAPALLOC-2-verdict-preregistration.md --type inquire
python scripts/check_brief.py docs/briefs/pre-registration/Q-CAPALLOC-2-verdict-preregistration.md
```
