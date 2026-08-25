# NOTICE 2026-08-25 — ox-alpha sanitized review: mechanism-first gate vs. historical iteration

**Notice ID:** N-2026-08-25-ox-alpha-mechanism-gate-overcorrection
**Observed:** 2026-08-25
**Author:** Cursor Cloud Agent (commission: "pose this question to ox-alpha, post the response")
**Type:** Notice-phase. External adversarial-lens review, reconciled against real repo state.
$0 · K=0 · no camp · no card. No live-risk surface touched.
**Status:** `RESOLVED` — reconciliation complete; no new candidate, no methodology change proposed;
one genuinely novel thread (gate-calibration probes) and one convergent framing (mechanism as a
priced prior across already-chartered lanes).

---

## §0 — Governance basis

Sent under [`docs/adr/2026-08-22-ox-alpha-adversarial-lens-scope.md`](../../adr/2026-08-22-ox-alpha-adversarial-lens-scope.md)
§2's **base scope** (adversarial second-opinion lens on a reasoning/judgment call) — not the
bounded-extension candidate-generation addendum. The operator supplied the question; it was
genericized further before send (no strategy / firm / date / dollar / campaign tokens; the
30–70% shrinkage band restated as "one-third to two-thirds"; the WHO clause restated as
"structurally compelled to take the losing side"). No mechanism ideas were requested.

**Amendment-first / dedup (this session, before authoring):**

```
$ python scripts/check_advisor_dedup.py --keywords "ox-alpha mechanism-first iteration gate over-correcting historical assets capped trial budget" --top 8
# nearest: generation-assumptions sweep; MNQ/SPX ledgers; Q-TRAINKILL-1; A1 kill-register
# audit. No prior ox-alpha consult owner for this question.

$ rg -n "ox-alpha-mechanism-gate|mechanism-uncertain|priced prior" docs/briefs/INDEX.md lab/CATALOG.md docs/notes/notice
# empty
```

Existing owner for the use-count is the ox-alpha ADR (addendum below). The reconciliation has no
prior owner — each sanctioned use gets its own notice, per standing pattern.

**Sanitization applied:** outgoing prompt sha256
`6325549b3f3aaab0b8d136d32c00baf037e9f2a86951471dee46f8d4c0f35162` (3,077 bytes). Fingerprint
sweep CLEAN (no operator name, no INQHIORI, no `dd_protection`, no strategy/firm names, no dates,
no dollar figures, no repo slug, no vendor/product names). Incoming content-channel fingerprint
CLEAN on the same denylist.

**Send/receive record:** `stealth/ox-alpha` via `https://openrouter.ai/api/v1/chat/completions`,
`$OPEN_ROUTER_API`, no `HTTP-Referer` / `X-Title`. HTTP 200, one attempt, 365.8s,
`finish=stop`. prompt_tokens=672 / completion_tokens=9,774 / content 11,605 chars /
reasoning 35,886 chars (not stored). `$0`. No transcript of the hidden-reasoning channel is
stored in-repo (standing bar). This notice holds the reconciliation, not the raw reply.

**Reconciled against (Rule 0, this session):**

| Artifact | Anchor |
|---|---|
| ox-alpha scope ADR | `984b6e8` (2026-08-24) |
| Deep-iteration lane charter | `f0a4386` (2026-08-23) |
| No-counterparty (blind) channel ADR | `fa0a363` (2026-08-23) |
| Mechanism-boundaries ADR (2-A four-clause) | `340722c` (2026-08-24) |
| A1 kill-register attribution audit | `00c8451` (2026-08-23) |
| Backtest→live shrinkage convention | `027a729` (2026-08-14) |
| Open-ended mining ox-alpha notice | `f23977c` (2026-08-24) |
| Deep-lane ox-alpha design-review notice | `540c794` (2026-08-24) |
| MSL wall-scope audit | read this session (13/14 walls hold; dryness = generation-input) |
| Family-K ADR | read this session (`K_eff = K_intrinsic`) |
| M-19 (methodology lessons) | read this session (floor is K-governed) |

---

## §1 — Reconciliation table

| # | ox-alpha claim | Real repo state | Verdict |
|---|---|---|---|
| F | Framing: the tension is five different objects (winner's curse, program-level multiplicity, holdout integrity, mechanism-as-prior, unrecorded-N identifiability) | Matches standing doctrine: DSR/K-ledger, `lesson_oos_gate` / `lesson_reporting_burns_holdout`, harvest Req 1a + 2-A four-clause (mechanism is a prior only if named before data), M-19 (unknown/high K makes the floor undefined or unreachable). | **Confirms existing.** Independent re-derivation of the estate's own vocabulary. |
| 1a | The mechanism gate is an *uncalibrated* filter stacked on a calibrated DSR floor, and it is the uncalibrated one doing the killing; its false-negative rate vs live risk-adjusted return has never been measured because gate-killed candidates are never tested | A1's taxonomy is finer than "mechanism vs DSR vs cost" (DIRECTION / SIZE / CADENCE / POWER / COST / REGISTRY / EVIDENCE). Four-clause admission deaths are zero-data; many other cells are cell-demonstrated. The DSR floor *does* bind on high-K mines (Q-GATECART-1 / M-19). Wall-scope audit: 13 of 14 MSL-era walls legitimately scoped; dryness is a **generation-input** problem, not over-tight evaluation. A1 revival list empty under two proposed SIZE/DIRECTION loosenings. | **Partial.** The "FN rate of the four-clause gate has never been measured by running rejected candidates through the pipeline" **survives as a named gap**. The inference "therefore the gate is over-correcting / most of the search space is closed" is **refuted** by wall-scope + A1. |
| 1b | Narratability is neither necessary nor sufficient; a competent analyst can write a compelled-loser paragraph; real diffuse effects fail the test | Why the [blind channel](../../adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md) exists (no-counterparty constructs; Req 1a untouched for anyone who *does* name a counterparty). ICT record is the in-house proof that narrative richness ≠ mechanism. 2-A alternatives table already rejected "keep 1a as-is, rely on downstream gates." | **Confirms existing** — independently derived. Does not license loosening 2-A. |
| 1c | Pattern-first discovery is historically how persistent anomalies were found; the historical program's failure was *validation*, not *discovery*; DSR + virgin holdout already repairs validation | The estate already opened both a pattern-first door (blind) and a bounded-iteration door (deep lane). The CFD-era iterative product is the worked counterexample that validation *and* uncontrolled search failed together: [decompound HOLD](../../adr/2026-06-07-decompound-remc-hold.md) H1 half (owner of the bust figure; do not restate). Deep-lane §1: "neither corner is adequate." | **Partial.** "Repair validation" was done. Residual dryness after opening both doors is not explained by a missing validation step. |
| 1d | Retention haircut is applied to the wrong conditional: the held book is live-validated, so population-mean shrinkage overstates decay for the selected tail | **Fact (1) as posed overstates live validation.** There is no live c1 book; no strategy-signal fill has occurred; the CFD estate is retired; the two futures legs are withdrawn. The shrinkage page is an *ex-ante planning prior* (McLean–Pontiff band), not a measured live/backtest ratio on the held book, and it already says search-intensity ↑ ⇒ retain *less*. Conditioning-on-live-success does not attach. | **Does not survive as stated.** Premise failed. The residue (do not use a population-mean haircut as a *pre-data kill rule*) is fair and already how the page is scoped — it is not a gate. |
| 2a | Citing the best-held strategies as evidence iteration works is circular; with N unrecorded the deflation integral is undefined | Exact deep-lane §1 + M-19 diagnosis. The locked CFD book is an unrecorded search; "we didn't write the trials down" ≠ "we had few trials." | **Survives as the binding Part-2 argument.** Already the estate's own position. |
| 2b | Live records are softer than they look (selection on having worked so far; tuning/live overlap; post-launch tweaks) | Stronger than sent: there is no live book to be "softer." Historical MC-anchor literals are historical record, not a current pass probability ([`docs/mc_anchor_history.md`](../../mc_anchor_history.md)). | **Survives, stronger than sent.** |
| 2c | Mechanism has Bayesian weight only if stated before data; iterate-then-explain is HARKing | 2-A: all four clauses named ex ante, before any data is read. Harvest Req 1a. | **Confirms existing.** |
| 2d | DSR assumes known, exchangeable N; the mechanism gate is the practical handle that keeps N small and non-arbitrary | M-19: floor is K-governed; "low-K, mechanism-first axes can pull the floor below plausible edge quality." Harvest "Confirm-not-mine." | **Confirms existing.** |
| 2e | Error asymmetry: a false admit pollutes the research commons (shared holdout / K); a false reject is silent | `K_eff` never shrinks; holdout burns on selection; abandoned campaigns still bank executed looks (2-C). | **Confirms existing.** |
| 3a | Demote mechanism from a binary gate to a *priced prior*; generation method sets the price of entry; a single-use confirm enforces apparent→true mapping for every candidate | The estate already has a discrete version of this dial: harvest/MSL (full 4-clause, typically one-shot), [deep lane](../../adr/2026-08-16-deep-iteration-lane-charter.md) (named family, declared K, one-shot confirm), [blind](../../adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md) (no counterparty claim, D-K1). There is no chartered "qualitative-mechanism / larger-K" middle tier, and deep still *requires* a named family — it does not admit mechanism-uncertain iteration. | **Convergent framing, not a new channel.** The priced-prior sentence is a cleaner description of the three-lane stack than most in-repo prose. Adopting a continuous dial or a no-mechanism K=16 tier needs its own ADR. |
| 3b | Hard caps: Tier A 256 / B 64 / C 16; z-thresholds 2.6 / 3.0 / 3.5 | Deep lane hard-caps `K ≤ 33` (M-19 Guardian-quality crossing) and `floor_at_k ≤ 2.0`. Blind is much tighter (D-K1 / Cap). Tier A at 256 sits between M-19's Guardian (33) and Aegis (441) crossings and would raise the floor toward the overfit-suspect zone the deep-lane conjunct (ii) exists to keep unreachable. | **Contradicts standing K-caps.** Illustrative defaults, not adoptable without superseding M-19 / deep-lane §2.2. |
| 3c | Charge *effective* K from the correlation structure of trial return vectors | Family-K: `K_eff = K_intrinsic`; deep-lane §2.2: every variant available to be chosen counts. Charging full K on correlated variants is a **ruled conservatism** (same finding as the 2026-08-24 deep-lane ox-alpha review, row 4). | **No** — ruled election, not a defect. |
| 3d | SEARCH/VAL/CONFIRM 60/20/20 with one optional O'Brien–Fleming VAL peek | Deep-lane + blind already freeze a train/confirm split and a single confirm read. Group-sequential / alpha-spending peeks were proposed on the 2026-08-24 deep-lane review and recorded as candidate governance input only — they contradict single-read doctrine. | **Recorded as candidate input only** (repeat). |
| 3e | Auxiliary-prediction channel (signs on other eras / instruments / sorts) lets a pattern *earn* a mechanism without burning CONFIRM | Harvest bundled predictions (placebo / instrument / covariance / micro) already do this for mechanism-first campaigns. 2-A clause 4 (HOW it dies) is the constraint-observable version. | **Confirms existing.** |
| 3f | **Gate-calibration probes:** reserve a fraction of annual evaluation budget for randomly selected mechanism-gate rejects, run blind through the same capped pipeline, to measure the gate's false-negative rate | Not present. Wall-scope tested whether walls are *licensed*; A1 tested whether two amendments would *revive* cells; neither ran rejected candidates through discovery. Q-CAPBAND-1's "gate-calibration" is a different object (gate-layer counterfactual, no candidate scored). | **Genuinely novel — open thread.** Not actionable now (would spend K/holdout on a measurement of the gate, against wall-scope's generation-input reading and A1's empty revival list). Recorded so it is not lost. |
| 3g | Legacy re-freeze: treat the held book's history as search, not confirmation; pre-commit a forward horizon as deferred confirmation | No venue remains for the CFD book; the futures editions are withdrawn. The decompound H1 result already *is* a failed out-of-regime confirmation of that book. A forward paper-log of a withdrawn book is not a live option. | **Blocked in practice.** The honest half (do not grandfather the pedigree as confirmation) is already how the estate treats that book. |
| S | Synthesis: the binary "is the gate right?" is ill-posed; the audit finding is consistent with both stories until the gate's accuracy is measured; bound the iteration, account for the trials, spend the holdout once | Deep-lane §1 in other words. The 2026-08-24 mining review independently reached the same "fast proposal / slow single-shot confirm" shape. | **Confirms existing.** |

---

## §2 — Net verdict

**No methodology change is proposed by this Use.** The question as posed is the same tension the
deep-lane charter already named and priced: uncontrolled iteration produced an uninterpretable
(and, on the H1 half, regime-fragile) book; one-shot mechanism-first has produced no successor;
the chartered middle is bounded-depth iteration *inside a named family*, survivor measured once
on an untouched confirm.

Ox-alpha's Part 1 is the strongest *form* of the over-correction argument the estate has been
given (uncalibrated narrative filter; unauditable FN rate; narratability ≠ edge). Its load-bearing
inferences do not survive contact with wall-scope, A1, the blind channel, or the actual live-ops
posture. Part 2 independently re-derives the estate's own binding argument and is stronger than
the prompt, because Fact (1)'s "live-validated" clause is false.

The Part 3 design is the deep lane plus three extras the estate has already accepted or
declined: a priced-prior *framing* of the existing three lanes (keep as description); correlation-
discounted K and sequential VAL peeks (already declined); and **gate-calibration probes** (new,
not-yet-actionable).

**Since this Use both confirmed existing discipline and surfaced one genuinely novel thread,
revert trigger (b) (three consecutive zero-value uses) does not tick.**

---

## §3 — What this does NOT license

- Does not open a card, camp, or manifest. $0 / K=0 by design.
- Does not amend 2-A, harvest intake, the deep-lane charter, the blind channel, M-19, or the
  shrinkage convention. The novel thread in §1 row 3f is a future-consideration pointer only.
- Does not authorize running rejected candidates through the discovery pipeline, raising any
  K cap, or treating the locked book as a live confirm.
- Carries zero authority over any admission decision, per the parent ADR §2/§5.

---

## §10 — Audit hooks (runnable)

```bash
# This notice exists and is the reconciliation owner
test -f docs/notes/notice/N-2026-08-25-ox-alpha-mechanism-gate-overcorrection.md && echo present

# Use-count pointer landed on the parent ADR
rg -n "N-2026-08-25-ox-alpha-mechanism-gate-overcorrection" docs/adr/2026-08-22-ox-alpha-adversarial-lens-scope.md

# Novel thread was not already named as a discovery-pipeline probe
rg -n "gate-calibration probe|randomly selected.*reject" docs/methodology/ docs/adr/ docs/notes/notice/

# Existing priced-prior stack (the convergent framing)
rg -n "lane deep|lane blind|mechanism-first" docs/adr/2026-08-16-deep-iteration-lane-charter.md docs/adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md lab/discovery/register_search.py | head

# Wall-scope generation-input reading this Use's Part-1 inference fails against
rg -n "generation-input" docs/notes/audits/programme-audit/2026-08-15-msl-wall-scope-audit.md
```

## Verification

```bash
python scripts/check_brief.py docs/notes/notice/N-2026-08-25-ox-alpha-mechanism-gate-overcorrection.md --type notice
```
