# Q-CAPALLOC-1 — pre-registration: is the c1 per-leg contract-cap allocation dominated?

**Status:** `FROZEN` (operator-signed 2026-07-27, §9). No item below changes after any candidate
cell is seen — amendments require closing this pre-registration and opening a fresh one
(Known Trap #12). The freeze is git-auditable: this file's commit strictly precedes any
`run_capalloc.py` execution (§10 hook 5).
**Authored:** 2026-07-27 · Claude Code (Opus 5), operator-directed
**Loop of record:** OUTER (INQHIORI) — measurement of a live constant, not a tempo decision.
**D-S-A domain:** data (measurement; candidate set + gate fixed pre-run). **Any live application
is a separate `system` change** requiring an amending ADR + operator GO — this brief cannot arm,
size, or edit anything.
**Artifact path:** `docs/briefs/pre-registration/Q-CAPALLOC-1-verdict-preregistration.md`
**Harness:** `lab/archive/c1_capalloc_2026-07-27/run_capalloc.py` (to be authored; imports the
kernels in `lab/analysis/c1/tradeify_book_composition_2026-07-23/gap_stage2_capbound.py`)

---

## §0 — Rule-0 reads (production source; verified this session 2026-07-27, HEAD `97ffaa7`)

Per the Q-COSTGEO-3 repair, each row states **the verification performed**, not merely the value.

| # | Artifact + anchor | Value consumed | Verification performed |
|---|---|---|---|
| 1 | `ops/c1_rail/c1_sizing_host_reference.py` @ `c134060` | `LEG_MAP` `cap_alloc` = MYM **69** / MNQ **11**; reserve law `floor(cap/(1+pyr/100))` (L7); pyramid 750% / 1000% | Read L1–100 in full. The split's stated rationale is L77–79 verbatim: *"MYM is favoured because it is granularity-tolerant and **carries the size**"*. L82–84 declares the split an **"UPGRADE PATH (not a permanent ceiling)"**. L72–73 states the cap branch is **invariant to the lifecycle rung**. |
| 2 | `lab/analysis/c1/q_rail_1_2026-07/f2_floors.json` @ `fd95c72` | MYM `ideal_base_at_100k_w1` 15.461 → `base_capped` **8**, add 60; MNQ 3.207 → **1**, add 10; `pre_2026_07_22_whole_cap_per_leg` MYM 9/67, MNQ reserve 7 | Parsed the full JSON. Confirmed `floor(69/8.5)=8`, `floor(11/11)=1`, `floor(80/8.5)=9`, `floor(80/11)=7` reproduce every published figure exactly. |
| 3 | `core/firm_rules.py` @ `cb60516` | `Tradeify_Select_100K`: `micro_contract_cap` **80**, `profit_target_pct` 6.0, `max_dd_pct` 3.0, `min_trading_days` 3, `consistency_rule_pct` 40.0 | Read the tier block verbatim (L319–330 + the 2026-07-22 re-verification comment block L237–290). |
| 4 | `lab/analysis/c1/tradeify_book_composition_2026-07-23/gap_stage2.py` @ `61424aa` | Eval/funded rule constants (L32–34) and the `eval_sim` / `funded_sim` / `build_paths` kernels | Read in full. Confirmed the sim's own cap model is a **day-aggregate clip** on panel qty (L108–111, L157–162), not the rail's per-leg reserve law — this is the gap Q-CAPALLOC-1 exists to close. Also confirmed the published headline is computed at `results[1.0]` (L255). |
| 5 | `lab/analysis/c1/tradeify_book_composition_2026-07-23/gap_stage2_capbound.py` — **UNCOMMITTED** (`git status` = untracked at authoring) | Verbatim ports of the four kernels above; per-trade rail-qty reconstruction | Authored + run this session. **Must be committed before §9 is signed** so the freeze is git-auditable. Its three controls are recorded in §7. |
| 6 | `docs/briefs/2026-07-23-tradeify-book-composition.md` @ `a68aadc` | 2-leg anchors: 63% eval pass / 8.2-mo median / 1.00 winning day-mo / $339 chain; funded start tier 40 micros until EOD ≥ $103,000 | Read §0–§7 + §10. Rule pins §0 carry three ⚠ secondary-sourced items (winning-day $200, funded start tier, Flex min payout) — **unresolved, and they bind this brief's funded-phase arm** (see §5 and §6 AMBIGUOUS). |
| 7 | `docs/adr/2026-07-17-c1-rail-build-account-registration-go.md` @ `153b64e` | c1 book deployed at WATCH-1 0.50×; attended-only; ceiling $700; B7 a separate GO | Read §Addendum 2026-07-22 + §Addendum 2026-07-24 (the corrected-geometry closes). |
| 8 | `docs/methodology/regime_robustness_gate.md` @ `f2be990` | Both-halves discipline: a lever passes only if it passes on **both** half-panels, each pinned to the brief floor | Read in full. This is the gate of record for §4 — chosen because full-panel is **burned** by the prior look disclosed in §7. |

**Not read, and why it does not bind:** locked Pine sources (`**/*.pine`, gitignored). The pyramid
ratios 750% / 1000% enter only through `LEG_MAP` (row 1, Tier-1 read) and are consumed as
**fixed inputs, never varied** — no Pine constant is re-derived here.

---

## §1 — Context + the question (symptom-only)

The per-leg cap allocation (MYM 69 / MNQ 11) was introduced 2026-07-22 to fix a real breach risk:
the host had been applying the whole 80-micro account cap to *each* leg, so the 2-leg book could
compute 153 micros against an 80 limit (1.91×). The fix was correct and is not in question.

The **split** chosen inside that fix is. Its stated rationale (§0 row 1) is that MYM "carries the
size." On the pinned venue-edition panels, MYM carries **$35,122** of the book's **$127,826** net
(27%); **MNQ carries $92,704 (73%)**. MYM carries the *contract count*; MNQ carries the *P&L*. The
split maximised cap utilisation (79 of 80 micros allocated) on the leg with the smaller share of
net, and its P&L cost was never measured — the sizing host's own comment justifies it on
cap-compliance grounds alone and explicitly labels it an upgrade path, not a ceiling.

MNQ's 1000% pyramid makes the reserve law quantize brutally: `floor(11/11) = 1`, so MNQ's base is
pinned at **1 contract at every lifecycle rung**, and it takes 22 allocated micros to reach base 2.

**Symptom-only phrasing:** *a live sizing constant was set on a premise that does not match the
book's measured P&L distribution, and its cost has never been measured.* This brief measures it.
It does not propose a replacement value, and it does not re-open the rung question.

---

## §2 — Prior art / lineage (cited, not re-decided)

- **`docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md`** — corrected trailing-DD
  geometry; §4 UNDISCHARGED, hard date 2026-11-08. Untouched here.
- **`docs/briefs/closures/Q-BUSTGATE-1-closure-falsified.md`** + **`docs/adr/2026-07-23-c1-rung-selection-ev-objective.md`** —
  the rung question (0.50× vs 1.00×), resolved to "keep 0.50× / accept NO-GO". This brief
  **does not re-open it** (see §5), but §7 discloses a measured fact that bears on its premise.
- **`docs/briefs/closures/Q-FUNNEL-1-closure-resolved.md`** — funnel-EV preferring 1.00×;
  computed on rung-scaled panel P&L.
- **`docs/briefs/closures/Q-COMPOSE-1-closure-falsified.md`** — bust-floor compose FALSIFIED;
  disposition c1-alone. Composition is frozen here; only the cap split varies.
- **`docs/briefs/closures/Q-COSTGEO-3-closure-ambiguous-needs-depth.md`** — the 67-lot MYM add is
  ~13× median displayed depth (D1 = 0.0% at 61 add-moments). **Directly relevant:** any candidate
  that *lowers* MYM's reserve also lowers that order's size, which is a liquidity improvement this
  brief must report but must not score (see §5).
- **Lessons that bind:** `lesson_snag_best_of_k_anchor_graveyard` (per-cut PASS after search = best-of-K),
  `lesson_reporting_burns_holdout` (characterisation tables ARE selection),
  `lesson_full_panel_masks_regime_split` (static levers pass pooled, fail on a half),
  `lesson_dsr_floor_k_governed`.

---

## §3 — Question (Q-CAPALLOC-1)

**Q-CAPALLOC-1:** What does the incumbent 69/11 per-leg cap allocation cost the c1 book in
time-to-payout and expected cash, and is it dominated by another allocation of the same 80-micro
account cap under the both-halves regime gate?

---

## §4 — Falsifiable hypothesis (H-CAPALLOC; binary)

**H-CAPALLOC — if** at least one candidate split from the §5 frozen enumeration satisfies **all
five** conditions below on **both** half-panels (H1 and H2) independently, **then** the incumbent
allocation is **dominated**, and the allocation routes to an amending ADR + operator GO as a
live-sizing change (sequenced per §8). **Otherwise** H-CAPALLOC is **falsified**: 69/11 stands as
ratified, the measured cost is recorded as the price of the 2026-07-22 compliance fix, and the
question closes without a live change.

Dominance conditions (all five required, on each half separately):

| # | Condition | Threshold |
|---|---|---|
| D1 | Median time to **first payout** (eval median + funded first-payout median) | ≥ **0.50 months** lower than incumbent |
| D2 | `E[cash]` (mean trader cash over the funded horizon) | ≥ **10%** higher than incumbent |
| D3 | Eval pass rate | ≥ incumbent **− 2.0 pp** |
| D4 | Funded mortality at 1 year | ≤ incumbent **+ 2.0 pp** |
| D5 | Max combined concurrent stack | **≤ 80 micros** (hard; the compliance invariant the 07-22 fix exists to protect) |

**Seed-noise floor:** every margin is measured against the **across-seed standard deviation**
reported by the harness (3 seeds, fixed 11/12/13). A margin smaller than 1 sd on either half is
**not a margin** and scores that condition FAIL. This is pre-declared, not applied post hoc.

**Falsified if:** zero candidates satisfy D1–D5 on both halves.
**Resolved if:** ≥1 candidate satisfies D1–D5 on both halves.
**Ambiguous if:** the conditions in §6 row 3 fire.

---

## §5 — The test (FIXED) + forbidden moves

### Frozen candidate set — 12 cells, zero researcher DOF

The panel P&L is constant within a reserve plateau, so the candidate set is the set of **distinct
reserve pairs** reachable under the account cap, each represented by its **minimum** `cap_mym`
(a mechanical canonicalisation rule — no researcher choice at any step):

```
res_mym = floor(cap_mym / 8.5)   res_mnq = floor((80 - cap_mym) / 11)
admit iff res_mym >= 1 AND res_mnq >= 1 AND (total max stack) <= 80
```

| # | res MYM/MNQ | canonical split | max stack | | # | res MYM/MNQ | canonical split | max stack |
|---|---|---|---|---|---|---|---|---|
| 1 | 1/5 | 15/65 | 63 | | 7 | 5/2 | 48/32 | 64 |
| 2 | 1/6 | 9/71 | 74 | | 8 | 5/3 | 43/37 | 75 |
| 3 | 2/5 | 17/63 | 72 | | 9 | 6/1 | 59/21 | 62 |
| 4 | 3/4 | 26/54 | 69 | | 10 | 6/2 | 51/29 | 73 |
| 5 | 4/3 | 37/43 | 67 | | 11 | 7/1 | 60/20 | 70 |
| 6 | 4/4 | 34/46 | 78 | | 12 | **8/1** | **68/12** | 79 |

Cell 12 **is the incumbent**: live 69/11 and canonical 68/12 yield the identical reserve pair
(8, 1) and therefore byte-identical sizing. It is the **control**, never a candidate.

### Fixed test parameters

| Item | Fixed value |
|---|---|
| Book | c1 2-leg exactly as deployed: Striker DJ30→MYM + Striker NAS100→MNQ, byte-pinned 2026-07-23 venue-edition exports. **Not re-weighted, not re-composed.** |
| Rung | **WATCH-1 0.50× only** — the last ratified rung. The 1.00× arm is **not run** (see forbidden moves). |
| Sizing law | `rail_base = min(panel_base, res_leg)`; `rail_add = floor(rail_base × pyr/100)`; `scaled_pnl = row_pnl × (rail_qty / panel_qty)`. Exact, not approximate — derivation and its proof are in the harness docstring. |
| Gating partition | **H1 and H2 half-panels, independently**, index-midpoint split, per `docs/methodology/regime_robustness_gate.md`. |
| Full panel | **Reported as diagnostic only. It cannot accept or reject** — burned by the §7 prior look. |
| Engine | `eval_sim` / `funded_sim` / `build_paths` ported verbatim from `gap_stage2.py` @ `61424aa`; Mon-anchored week-block bootstrap; seeds 11/12/13; `n_paths` 6,000; `h_eval` = `h_fund` = 2,600 bd. |
| Rule constants | `gap_stage2.py` L32–34 unchanged, including the three ⚠ secondary-sourced pins. |
| Reported per cell | eval pass %, eval median (bd + mo), first-payout median, never-paid %, dead@1y, `E[cash]`, max stack — each with across-seed sd. |

### Forbidden moves (each genuinely tempting this session)

- **Selecting the sweep argmax (17/63, $95,907 full-panel net).** It is the largest number I saw
  and it is best-of-69 on burned in-sample data. Forbidden: the verdict is a **dominance** claim
  against a named incumbent, never an argmax claim. If cell 3 also happens to satisfy D1–D5 it
  qualifies like any other cell — its sweep rank grants it nothing.
- **Refining the cap grid to "find the true optimum."** More K on burned data; buys precision the
  evidence cannot support.
- **Promoting the full-panel result to the gate if the halves disagree.** The full panel is where
  the prior look happened, and it is exactly the failure mode `lesson_full_panel_masks_regime_split`
  names.
- **Re-opening the 0.50× / 1.00× rung on the strength of §7's rung-inertness finding.** Tempting —
  the finding shows the rung barely moves live size, which invites "so just flip it." That is a
  separate, already-ratified question (`docs/adr/2026-07-23-c1-rung-selection-ev-objective.md`);
  §7 records the fact for the operator and claims nothing from it.
- **Scoring the MYM-add liquidity improvement.** Lower MYM reserve shrinks the 67→60→smaller add
  that Q-COSTGEO-3 flagged at ~13× displayed depth. Real, and it is **reported**, but it is not in
  D1–D5: it was not pre-registered as an objective and adding it after the fact would be an
  outcome-conditional criterion.
- **Landing any `LEG_MAP` edit inside this brief, or before B7-REFIRE validates the chain.**
  Sequencing is §8; the brief has no arming authority under any verdict.
- **Touching the locked pyramid ratios (750% / 1000%) to relieve MNQ's quantization.** They are the
  parameter axis; the whole quantization problem is downstream of them and must stay so.
- **Treating the three ⚠ unverified rule pins as verified** because the sim consumes them. They are
  inherited uncertainty and they gate the funded arm — see §6.

---

## §6 — Gate criteria (binary dispositions)

| Verdict | Trigger | Disposition |
|---|---|---|
| **RESOLVED-INCUMBENT-DOMINATED** | ≥1 candidate satisfies D1–D5 on **both** halves, all margins ≥ 1 sd | Route to operator + amending ADR for the `LEG_MAP` change. Sequenced **after** B7-REFIRE Stage 2 (§8). ADR must re-pin `f2_floors.json` and re-run `pytest tests/ops/ tests/rail_crosstrade/` in the same commit. |
| **FALSIFIED-INCUMBENT-STANDS** | Zero candidates satisfy D1–D5 on both halves | 69/11 stands as ratified. Record the measured cost of the 07-22 compliance fix in the GO ADR as an addendum. No live change. Capture the lesson candidate in §2's registry. |
| **AMBIGUOUS** | Any of: (a) a candidate passes on exactly one half; (b) the best candidate's decisive margin is < 1 sd on either half; (c) the incumbent control cell fails to reproduce this session's measured figures (12.2 mo eval median / 5.5 mo first payout / $32,904 `E[cash]`, ±1 sd) — harness defect, no verdict; (d) the verdict flips under any of the three ⚠ unverified rule pins in a pre-committed sensitivity pass | (a)/(b): report and hold; re-test gated on the first 6 months of live fills, not on a re-run. (c): fix the harness, no verdict. (d): **the dashboard rule-pin verification (`docs/notes/2026-07-24-tradeify-rulepin-verification.md`) becomes a hard blocker** on the live change. |

**Pre-registered before any candidate cell runs.** Amending §4 or §6 after seeing candidate results
requires closing this pre-registration AMBIGUOUS and opening a fresh one (Trap #12).

---

## §7 — Prior-look disclosure + K accounting (load-bearing — read before scoring)

**This is not a first look. The full panel is burned.** On 2026-07-27, before this
pre-registration was authored, the following were run and their results seen:

1. **A 69-cell full-panel net sweep** over `cap_mym ∈ [11, 79]`. Results seen: incumbent 69/11
   **$55,206**; plateau 43/37–47/33 (reserve pair 5/3) **$85,917**; argmax 17/63 **$95,907**.
2. **Full-panel MC on exactly two cells** — 69/11: eval pass 80.3%, median 12.2 mo, first payout
   5.5 mo, never paid 14.9%, dead@1y 25.0%, `E[cash]` $32,904. 45/35: 80.5%, 10.3 mo, 4.8 mo,
   17.5%, 25.2%, $44,358.
3. **A rung-inertness check.** Flipping 0.50×→1.00× changes total contracts sent by **+0.17%** on
   MYM (15,410→15,436) and **exactly 0%** on MNQ; 222/227 MYM and 217/217 MNQ base entries are
   cap-bound at both rungs. Live corroboration: B6 (07-20, pre-split) filled MYM **9** =
   `floor(80/8.5)`; the 07-27 SIM filled MYM **8** = `floor(69/8.5)`.

**K accounting.** K_looked = **69** (net sweep) **+ 2** (full-panel MC cells). Candidate-set
membership carries **zero** DOF (structural enumeration, §5). The gating partition — **H1/H2
half-panels — was never computed for any split**, and is therefore the one dimension not burned;
this is precisely why §4 gates on the halves and §5 forbids the full panel from accepting or
rejecting. No DSR/SPA claim is made: the verdict is a **dominance test against a single named
incumbent**, not a best-of-K selection, and dominance on both halves at a pre-declared tolerance
is the strongest gate available on a panel this contaminated.

**Honesty limit that no design here removes.** With the full panel burned, a both-halves PASS
establishes *dominance robust across two regimes*; it does **not** establish that the winning cell
is optimal, and it cannot rule out that the plateau structure itself is an artifact of this panel's
composition. The forward check is live fills, not another re-run — §10 hook 6.

**Controls already passing** (from `gap_stage2_capbound.py`, this session): reconstruction of
`gap_stage1`'s `combined` column to **max |daily diff| = $0.00**; the published 63% / 8.2-mo anchor
reproduced at **64% / 8.2 mo** at the brief's own `h_eval=520`; rail sizing max stack **68 ≤ 80**.

---

## §8 — Run protocol + sequencing

1. **Commit `gap_stage2_capbound.py` and this file** before any candidate cell runs (freeze must
   be git-auditable — `lesson_prereg_freeze_and_confound_control`).
2. Author `lab/archive/c1_capalloc_2026-07-27/run_capalloc.py` importing the kernels; it must
   **not** edit `gap_stage2.py` or `gap_stage2_capbound.py` in place.
3. Run all 12 cells × {H1, H2, full} × 3 seeds. Emit `RESULTS.md` + `measured.json` citing this
   pre-registration by path and commit hash.
4. Apply §6 mechanically. Route the verdict to the operator.
5. **Sequencing — this brief does not block B7.** B7-REFIRE Stage 1/2 validate the *chain*;
   changing sizing days before the first armed strategy fill would conflate two experiments and
   add risk to the one that is already gated and dated. Any `LEG_MAP` change lands **after** the
   first live fill is banked, under its own ADR, with `f2_floors.json` re-pinned and
   `pytest tests/ops/ tests/rail_crosstrade/` green in the same commit.

---

## §9 — Authorization (operator directive of record)

```
AUTHORIZED / FROZEN: 2026-07-27 / JA (operator chat directive, this session, verbatim):
"commit them as-is with §9 signed"
Scope: measurement only. No LEG_MAP edit, no arming, no rung change, no Pine touch.
```

Signed **before** any candidate cell has been run. The two full-panel cells and the 69-cell net
sweep that predate this signature are **not** candidate-set results — they are the disclosed
prior look enumerated in §7, and they are why §4 gates on the halves rather than the pooled panel.

---

## §10 — Audit hooks (runnable)

```bash
# 1. Incumbent split unchanged in production (the control cell's premise).
grep -n "cap_alloc" ops/c1_rail/c1_sizing_host_reference.py

# 2. The rationale this brief tests is still the one in production.
grep -n "carries the size\|UPGRADE PATH" ops/c1_rail/c1_sizing_host_reference.py

# 3. Reserve law reproduces every published F2 figure (8/1 live, 9/7 pre-07-22).
python -c "import math; print([math.floor(c/8.5) for c in (69,80)], [math.floor(c/11) for c in (11,80)])"
# Expected: [8, 9] [1, 7]

# 4. Candidate set is reproducible from the frozen rule with zero DOF (expect 12).
python -c "
import math; s={}
for cm in range(9,70):
    rm,rn=math.floor(cm/8.5),math.floor((80-cm)/11)
    if rm<1 or rn<1: continue
    if rm+math.floor(rm*7.5)+rn+math.floor(rn*10)>80: continue
    s.setdefault((rm,rn),cm)
print(len(s), sorted(s.items()))"

# 5. Freeze precedes results (git-auditable, per lesson_prereg_freeze_and_confound_control).
git log --format='%h %ci' -- docs/briefs/pre-registration/Q-CAPALLOC-1-verdict-preregistration.md
git log --format='%h %ci' -- lab/archive/c1_capalloc_2026-07-27/RESULTS.md
# Expected: the pre-registration commit strictly precedes the RESULTS commit.

# 6. Forward check (replaces any re-run): realized per-leg fills vs the modeled split.
grep -rn "decision" /data/c1_rail_events.jsonl | head   # on the host, post-B7

# 7. The three unverified rule pins that gate the funded arm (§6 AMBIGUOUS row d).
grep -n "fill" docs/notes/2026-07-24-tradeify-rulepin-verification.md
```

---

## Verification

```bash
PYTHONIOENCODING=utf-8 python scripts/check_brief.py \
  docs/briefs/pre-registration/Q-CAPALLOC-1-verdict-preregistration.md --type inquire

# §0 anchors (Rule-0 confirmation)
git log -1 --format='%h %ci' -- ops/c1_rail/c1_sizing_host_reference.py                 # c134060
git log -1 --format='%h %ci' -- lab/analysis/c1/q_rail_1_2026-07/f2_floors.json    # fd95c72
git log -1 --format='%h %ci' -- core/firm_rules.py                              # cb60516
git log -1 --format='%h %ci' -- lab/analysis/c1/tradeify_book_composition_2026-07-23/gap_stage2.py  # 61424aa
git log -1 --format='%h %ci' -- docs/methodology/regime_robustness_gate.md      # f2be990

# Cross-reference: the net split this brief rests on (MYM 27% / MNQ 73% of book net)
python lab/analysis/c1/tradeify_book_composition_2026-07-23/gap_stage2_capbound.py | head -3

# Live-ops invariant: this brief touches no rail surface.
# NOTE (Trap M-AHF, caught at authoring 2026-07-27): the obvious form of this hook —
# `grep dry_run ops/data/c1_rail_config.json` — is NOT runnable. That path exists in no
# tree; only *.example.json are tracked, and the live config lives on the Fly volume
# (`ops/c1_rail/c1_rail_arm.py` DEFAULT_CONFIG_PATH = /data/c1_rail_config.json). The same broken
# command is currently published in `.claude/skills/c1-rail/SKILL.md` §Verification.
git ls-files | grep c1_rail_config     # expect: ONLY deploy/... and docs/... *.example.json
grep -n "DEFAULT_CONFIG_PATH" ops/c1_rail/c1_rail_arm.py   # expect: /data/c1_rail_config.json
git status --short -- ops/ core/       # expect: empty (no rail or locked-surface edit)
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-27 | Drafted. Candidate set frozen by structural enumeration (12 cells, zero DOF); gate set to both-halves dominance vs the named incumbent because §7's 69-cell full-panel sweep burns the pooled panel; rung fixed at the ratified 0.50×; live application explicitly sequenced after B7. | Claude Code (Opus 5), operator-directed |
| 2026-07-27 | §9 signed → `FROZEN`; committed unrun. Verification-block hook corrected at authoring after Trap M-AHF fired on it (the published `ops/data/c1_rail_config.json` path is dead — same broken command still in `.claude/skills/c1-rail/SKILL.md`, operator taking it separately). | Joshua (directive) + Claude Code (Opus 5) |
