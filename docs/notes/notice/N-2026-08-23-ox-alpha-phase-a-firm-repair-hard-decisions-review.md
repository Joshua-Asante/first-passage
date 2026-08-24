# NOTICE 2026-08-23 — ox-alpha sanitized review: three hard-decision judgment calls (Phase A / §4 firm-repair)

**Notice ID:** N-2026-08-23-ox-alpha-phase-a-firm-repair-hard-decisions-review
**Observed:** 2026-08-23
**Author:** Claude Code (Sonnet 5), operator direction ("send the hardest decision elements to
ox-alpha, generalized with enough context to be useful")
**Type:** Notice-phase. External adversarial-lens review, reconciled against real repo state.
$0 · K=0 · no camp · no card. No live-risk surface touched.
**Status:** `RESOLVED` — reconciliation complete; several objections survive, one high-value
concrete objection independently checked and does **not** survive against the real engine.

---

## §0 — Governance basis

Sent under [`docs/adr/2026-08-22-ox-alpha-adversarial-lens-scope.md`](../../adr/2026-08-22-ox-alpha-adversarial-lens-scope.md)
§2's **base scope** (adversarial second-opinion lens on reasoning/methodology, not a drafted
artifact verbatim but the judgment calls embedded in one) — not the separate, already-once-used
bounded-extension addendum (candidate generation). The ask was framed as "find the weakest links
in this reasoning" across three scenarios, never as a request for new strategy/mechanism ideas.
No fresh bounded-extension authorization was invoked or needed.

**Sanitization applied:** no firm name (Tradeify/Bulenox/BluSky/MFFU), instrument ticker, dollar
figure, percentage, or internal naming (Phase A, MSL, A1/A2/A3/R1/R2/R3, the 2026-11-08 date)
appears in the sent prompt. All three scenarios were rewritten as generic financial-evaluation-
product / generic-audit / generic-account-tier framings. No proprietary content is reconstructable
from the sent prompt or the response. Prompt text: `ox_alpha_hard_decisions_prompt.txt`
(scratchpad, not committed).

**Send/receive record:** `stealth/ox-alpha` via OpenRouter chat-completions, 2026-08-23.
prompt_tokens=1,078 / completion_tokens=12,598. finish_reason=stop. Took ~491s to return content
(model burns real budget on hidden reasoning before content appears — consistent with prior-use
notes in this repo's memory). First two send attempts hung indefinitely for reasons unrelated to
the model itself (a local PowerShell `-File`-invocation pathology in this session's sandboxed
background-execution path — diagnosed and worked around; not a repo-relevant finding). No
transcript of the hidden-reasoning channel is stored in-repo, matching this ADR's prior
no-transcript-for-reasoning-channel precedent.

---

## §1 — Reconciliation table

| Scenario | ox-alpha objection | Real repo state | Survives reconciliation? |
|---|---|---|---|
| 2 (A2 feasibility map) | Consistency-rule scorer may be **self-violating at day 1** if implemented as a naive continuous per-day check against still-small cumulative profit — named as the single highest-prior-probability failure mode, and a scorer bug of this shape would make the region spuriously empty. | Checked directly against `core/mc/simulation.py:186-196` (`simulate_path`, the real, unmodified, previously-battle-tested production engine — A2's own RESULTS.md §3 confirms it is reused, never reimplemented at this layer). The check fires **once**, only at the day the profit target is first reached, comparing that day's running `max_day_profit` against `consistency_frac × total_profit` **as of that same crossing** — not a continuous per-day check from day 1. An instant one-day target-hit *does* correctly fail (as a real consistency rule should); a multi-day path with the profit spread out correctly passes. This is also independently confirmed by real historical behavior: the same engine has produced genuine passes on real multi-year Striker backtests (median ~17 months to pass on one leg), which would be impossible under the pathological reading ox-alpha assumed. | **No** — the generic scenario framing invited a real risk class, but this repo's specific practice (reuse the frozen, already-proven engine rather than reimplementing scoring logic) is exactly what defends against it here. Recorded as a validation of the reuse discipline, not a defect. |
| 2 | Trailing-DD scored on open vs. closed equity is a distinct real risk (products differ; open-equity trailing is materially tighter). | A2's RESULTS.md §3 states the intraday-honest limb (`intraday_low`) is threaded throughout, "never close-only." | **No** — already handled by design, consistent with this repo's own W1 intraday-honest discipline. |
| 2 | Sweeping only **stationary** payoff-shape parameters (fixed win rate/shape/cadence/risk per cell) is structurally biased toward under-finding feasibility for a Goodhart-shaped consistency rule — state-dependent policies (throttle activity once the constraint is close to binding) are a different, likely more permissive, hypothesis class this sweep cannot express. | Task A2's own text (`docs/superpowers/plans/2026-08-23-viable-strategy-phase-a-target-derivation.md`) scopes the axes as static coverage, not adaptive. The actual run found a non-empty region (e.g. `wr0.70_bounded_clustered_cd8_rk250` clears `FEASIBLE` on both firms), so this is not an urgent live gap for this result, but it is a real, unaddressed limitation of what was scoped. | **Open — a genuine, real limitation**, not previously named anywhere in this repo's methodology docs. Worth recording as a follow-up axis if a future sweep needs a wider hypothesis class, not an action for this run (the region was not empty, so the emptiness-diagnosis machinery in the same answer does not currently apply). |
| 3 (R2 lock-scope) | Correct evidentiary bar needs (a) full-corpus textual isolation, (b) a **dependency trace** of every downstream consumer of the model's output that might touch post-pass quantities, (c) a **counterfactual invariance check** (assume the funded-stage rule also binds in qualification; diff every affected conclusion) — the "vacuous truth" risk: if nothing downstream ever touches post-pass quantities, the finding is safe, but that itself needs to be checked, not assumed. | R2's actual audit note (`docs/notes/audits/2026-08-23-bulenox-lock-scope-resolution.md`) did (a) rigorously — re-fetched both Wayback primary sources live rather than trusting Q-FIRMEOD-1's paraphrase, confirmed the lock language is textually scoped to the Master-stage page and absent from Qualification's own trailing-drawdown description, and confirmed `simulate_path` terminates at "pass" with no post-pass stage threaded at all. It does **not** contain a written dependency trace or a counterfactual-perturbation check — grepped for "downstream"/"counterfactual"/"dependency" in the note, zero hits. | **Open — a real, cheap, actionable gap.** R2's textual-isolation work is solid and independently verified; the dependency-trace/counterfactual step ox-alpha names would close the "vacuous truth" risk explicitly rather than leaving it implicit. Worth a short follow-up pass, not a re-open of R2's own conclusion. |
| 1 (A3, conditional) | The audit gating A3's own trigger condition is self-interested (whoever tags "inherited vs. demonstrated" knows the tag gates a desired relaxation) — recommends dual independent rating with an agreement statistic, blind reproduction of a subsample, and a **bidirectional** test (does the new screen also tighten currently-accepted cases, not just loosen rejections). | Task A1's own forbidden-moves list already separates attribution from re-scoring ("this is attribution, not re-testing") and treats an empty revival list as a valid, decisive outcome — but has no dual-rater/blind-reproduction step, and Task A3's own text has no bidirectional-test requirement. | **Open — genuinely novel, actionable if A3 is ever taken up.** The bidirectional-test suggestion in particular ("a genuine precision improvement should flag some currently-accepted cases as marginal too, not just loosen rejections") is not previously stated anywhere in this repo's methodology docs and is a sharp, cheap litmus test. |
| 1 | A3's own revert trigger ("zero revived cells produce even a preliminary positive within a window") is framed generically in a way that, read literally, would almost never fire (P(≥1 noise-level positive) ≈ 1 across N reopenings), and conflates "the screen was over-broad" (a logical claim) with "the reopened cells have edge" (an empirical claim). | The real trigger text (Task A3) is **stricter** than the generic framing sent: "zero revived cells have produced even a **G0 freeze**" — G0 is a real, costly, structural pre-registration-freeze milestone in this repo's own pipeline, not a noise-level p-value blip. The genericization in the sent prompt ("preliminary positive signal") understated how strong the real bar is. | **Partially survives** — the underlying conflation point (screen-validity vs. edge-existence are different claims and should have separately-stated criteria) is still worth naming explicitly in any future A3 ruling, but the near-unfalsifiability critique is weaker against the real G0-freeze bar than against the sanitized paraphrase. Recorded so a future reader does not treat the stronger critique as applying at full force. |
| 1 | Amendment (b)'s "contractual, not discretionary" premise about margin/limit-file triggers is an empirical claim needing historical-episode evidence, plus point-in-time reconstruction integrity and a strict knowability cut (file public *before* the trigger timestamp) to avoid admitting look-ahead triggers. | Task A3's actual text does not name either check. | **Open — genuinely new, concrete, and cheap** if amendment (b) is ever pursued. |

## §2 — What actually survives, net

The single most consequential objection (Scenario 2's day-1 scorer-bug concern) **does not
survive** — checked directly against the real, unmodified production engine and against real
historical pass evidence, not just against a description. This is itself a useful result: it is
a live demonstration that this repo's "reuse the frozen engine, never reimplement scoring logic"
discipline is doing real defensive work, not just ceremony.

What **does** survive, as live, cheap, worth-considering threads (none change any verdict already
reached; none block or reopen A1/A2/R1/R2 as executed):

1. **A3 bidirectional-screen test** — if A3 is ever taken up, require the new screen to also flag
   some currently-*accepted* cases as marginal, not just loosen rejections, as the sharpest
   available discriminator between a real precision improvement and dressed-up scope creep.
2. **A3 revert-trigger conflation** — separate "the screen was over-broad" from "the reopened
   cells have edge" as two different claims needing two different criteria, if/when A3's ruling is
   drafted; note the real G0-freeze bar is stronger than a naive reading suggests.
3. **A3 amendment (b) empirical premises** — "contractual not discretionary" and point-in-time
   file-reconstruction integrity need their own historical-episode check before Amendment 2 is
   adopted, not stipulation.
4. **R2 dependency trace / counterfactual check** — a short, cheap follow-up (enumerate what
   downstream consumers of the pass/fail model touch post-pass quantities; perturb the funded-stage
   rule into the qualification model and diff conclusions) would close the "vacuous truth" risk
   explicitly rather than leaving it implicit. Does not change R2's answer; strengthens its basis.
5. **A2 hypothesis-class limitation** — stationary-parameter sweeps are structurally biased toward
   under-finding feasibility for Goodhart-shaped consistency rules; a future extension sweeping
   state-dependent (adaptive) policies would be a strictly wider, more permissive search. Not
   urgent (this run's region was not empty), but real.

**Since this Use produced several objections that survive reconciliation, revert trigger (b)
(three consecutive zero-value uses) does not tick.**

---

## §3 — What this does NOT license

- Does not reopen A1, A2, R1, or R2 as already executed and reviewed this session — every gate
  verdict each task reached stands.
- Does not authorize drafting Task A3 — A3 still needs its own separate operator ruling regardless
  of anything in this notice, per the parent plan's own text.
- Does not authorize a fresh R2 re-derivation — item 4 above is a suggested cheap follow-up, not a
  finding that R2's conclusion is wrong.
- Carries zero authority over any decision, per the parent ADR §2/§5 — every item above is
  candidate-objection-grade input, to be weighed by the operator like any other input.

---

## §10 — Audit hooks (runnable)

```bash
grep -n "consistency_frac" core/mc/simulation.py | head -5
sed -n '186,196p' core/mc/simulation.py
grep -n "FEASIBLE" lab/analysis/c1/shape_feasibility_map_2026-08/RESULTS.md | head -5
grep -riE "downstream|counterfactual|dependency" docs/notes/audits/2026-08-23-bulenox-lock-scope-resolution.md   # expect: empty (confirms the gap)
```

## Verification

```bash
python scripts/check_brief.py docs/notes/notice/N-2026-08-23-ox-alpha-phase-a-firm-repair-hard-decisions-review.md --type notice
```
