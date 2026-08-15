# CC Handoff — Aegis-6J Wave-1 N≥80: exception vs fresh pre-reg

**Date:** 2026-07-16  
**Parent session:** Cursor (Joshua + Auto) — Wave-1 TV sweep closed FALSIFIED; operator asked pros/cons of exception given sel N 73–74 vs bar 80  
**Spawn target:** Claude Code (adjudicate — design/spec; do **not** implement a fresh pre-reg or amend frozen bars unless Joshua explicitly GO after your verdict)  
**Repo:** `multi_firm_operations`  
**Checkout:** branch `cursor/aegis-6j-wave1-falsified-close` (tip includes Wave-1 FALSIFIED close + this handoff; push before CC if CC needs remote)  
**Brief type:** CC handoff (single-step adjudication)  
**Parent question:** Aegis→6J prop reconstruction Stage-1 H-SWEEP — post-close process question  
**Authority:** Joshua (CEO). Cursor authored this brief; CC adjudicates. No commit/merge/push without Joshua's go.

---

## §0 — Rule 0 reads (PHASE 0 — before any recommendation)

Read and cite in your first response (paths + `git log -1` on each):

1. `docs/briefs/pre-registration/2026-07-16-aegis-6j-prop-reconstruction-prereg.md` — Status line; §2.5 windows; §2.6 filters (a)–(e) especially **(d) N ≥ 80**; §6 Stage-1 FALSIFIED branch; Trap #12 language; change-history close row.
2. `docs/briefs/closures/2026-07-16-aegis-6j-prop-reconstruction-stage1-falsified.md` — full closure (binding fail = sel N 73–74; degeneracies; forbidden moves).
3. `lab/analysis/aegis/aegis_6j_prop_reconstruction_2026-07/SWEEP_LOG.md` — cell table + degeneracy pairs + filter outcome.
4. `lab/analysis/aegis/aegis_6j_prop_reconstruction_2026-07/wave1_metrics.json` — confirm unique sel_n ∈ {73,74}, PASS_d all false, PASS_all all false.
5. `lab/analysis/aegis/aegis_6j_prop_reconstruction_2026-07/BASELINE_68f0e.md` — Stage-0 ENVELOPE-YES; note Stage-0 N≥80 was on **full span** (~130), not the selection window.
6. `docs/superpowers/plans/2026-07-16-aegis-6j-prop-reconstruction.md` — Task 2 checkboxes / FALSIFIED annotation.
7. Known Trap #12 doctrine as cited in the pre-reg (no post-result gate moves on a frozen artifact).

Optional cheap falsifier (≤2 min):  
`python -c "import json; m=json.load(open('lab/analysis/aegis/aegis_6j_prop_reconstruction_2026-07/wave1_metrics.json')); print(sorted({r['sel_n'] for r in m}), sum(r['PASS_all'] for r in m))"`  
Expect: `{73, 74}` and `0`.

After Phase 0: post a short read-report. Then answer §2. Do **not** draft a new pre-reg body in Phase 0.

---

## §0.5 — Clarifying questions (HALT-ON-AMBIGUITY)

Ask Joshua before recommending if any of these are unclear after Phase 0:

- **Scope of “exception”:** does he mean (A) informal override under the *same* frozen pre-reg and claim H-SWEEP RESOLVED anyway, or (B) close-and-reopen a **fresh** pre-reg with a re-justified N bar / window, disclosing this FALSIFIED run as prior-look?
- **Downstream intent:** if N is cleared, is the next step Stage-2 solo Part A on Tradeify+MFFU under the *same* selection rule (max mean qty among survivors), or is he only asking process/epistemics?
- **N bar redesign:** if (B), is he open to (B1) lower bar (e.g. ≥70), (B2) move (d) to **full-span** N≥80 (already clears), or (B3) drop (d) because sel N is uniform across cells?

If unambiguous from context, state your assumed default and proceed; prefer asking once over guessing.

**Recommended default if he does not answer before you write:** treat the live question as **(B) fresh pre-reg only** — never (A). Adjudicate whether (B) is *warranted* given 73–74 vs 80, and which of B1/B2/B3 is least Trap-#12-toxic.

---

## §1 — Context

Wave-1 (frozen c01–c12) was run on TV Deep Backtesting. Operator accepted Stage-1 **FALSIFIED** and closed: every cell fails filter **(d)** selection-window N ≥ 80 (actual **73–74**). Envelope / maxDD / holdout pass. Operator-confirmed degeneracies: c02≡c04, c05≡c06 (0.55% on screen), c11≡c12. Nine unique sha cover twelve labels.

Joshua then asked whether making an **exception** is reasonable because the sample is “not far off.” Cursor outlined pros/cons (uniform N across cells; ~8% short; Trap #12 / post-hoc bar move). He wants **your** adjudication from the artifacts — not a re-derivation of the sweep.

**What CC must produce:**
- A short written verdict: **NO-EXCEPTION (keep closed)** vs **FRESH-PREREG-OK (with preferred N/window redesign)** vs **NEEDS_CONTEXT**.
- Explicit reasoning against Trap #12 and against the signed §6 FALSIFIED trigger.
- If FRESH-PREREG-OK: one recommended redesign (B1/B2/B3 or better), with what must appear in prior-look, and what must **not** be claimed about the closed pre-reg.
- Return status per §6.

**What CC must NOT do:**
- Amend the frozen pre-reg’s N≥80 in place.
- Pick a Wave-1 “winner” or run Stage-2 Part A.
- Touch `core/`, allocations, `dd_protection`, Pine lock surface, or `ACTIVE_FIRM`.
- Commit, push, or open a PR (unless Joshua explicitly asks after adjudication).
- Soften the closed FALSIFIED record.

---

## §2 — Execution plan

### Step 2.1 — Adjudicate

- **Inputs:** §0 artifacts + Joshua’s question (“sample size not far off — pros/cons of exception”).
- **Action:** Decide whether any path that continues toward Stage-2 is methodologically sound, and which path.
- **Expected output:** Verdict block (see §6) + ≤1 page reasoning.
- **Per-step gate:** Verdict must name the closed §6 trigger and say whether 73–74 vs 80 is a *measurement near-miss* that justifies a **new** freeze, or a *gate that already fired* and should stay closed without reopen.

### Step 2.2 — If FRESH-PREREG-OK, specify the reopen packet (spec only)

- **Action:** List the minimum fields a fresh Stage-1 pre-reg must freeze before any re-selection (N bar or window definition; whether degeneracies are declared collapses; selection rule unchanged or not; prior-look mandatory cites to SWEEP_LOG + this closure).
- **Expected output:** Bullet checklist — not a full drafted pre-reg unless Joshua asks in-thread.
- **Per-step gate:** Checklist must make Trap #12 satisfaction mechanical (old pre-reg stays CLOSED-FALSIFIED; new artifact gets its own §9).

---

## §4 — Falsifiable hypothesis (under adjudication)

Not a new Pre-Q. Restate the **already-fired** Stage-1 gate for reference:

**H-SWEEP (frozen):** ≥1 of c01–c12 clears (a)–(e); max mean qty yields one winner.  
**FALSIFIED if:** zero cells clear (a)–(e) — **FIRED** (all fail (d)).  
**This handoff asks:** given fire already accepted, is a *new* pre-reg with a different (d) epistemically honest, or does “exception” equal post-hoc gate shopping?

---

## §5 — Forbidden moves

- In-place edit of N≥80 / selection window on the closed pre-reg.
- Claiming H-SWEEP RESOLVED under `2026-07-16-aegis-6j-prop-reconstruction-prereg.md`.
- Selecting a winner from the FALSIFIED grid “for discussion” that could leak into Stage-2 without a new §9.
- Treating Stage-0 full-span N≥80 as satisfying Wave-1 (d) without an explicit redesign that says so.
- Expanding into Class-S compose / MYM+MNQ / rail / go-live.

---

## §6 — Return taxonomy

- `DONE` — verdict delivered; no repo writes.
- `DONE_WITH_CONCERNS` — verdict delivered; flag residual risk (e.g. reopen still looks like shopping).
- `NEEDS_CONTEXT` — §0.5 ambiguity blocks verdict.
- `BLOCKED` — artifacts missing / branch tip wrong / hashes don’t match SWEEP_LOG.

**Verdict labels (put one on top of your answer):**
- `NO-EXCEPTION` — leave Stage-1 closed; no reopen now.
- `FRESH-PREREG-OK` — reopen allowed only via new pre-reg; state preferred (d) redesign.
- `NEEDS_CONTEXT` — ask Joshua the §0.5 questions.

---

## §7 — Spec-compliance / quality

Parent will check: you did not amend frozen bars; you did not authorize Stage-2; you addressed Trap #12 explicitly; you distinguished informal exception vs fresh pre-reg.

---

## Paste-ready opener (optional)

```
Checkout branch cursor/aegis-6j-wave1-falsified-close (latest tip).
Execute the CC handoff: docs/briefs/handoffs/2026-07-16-cc-handoff-aegis-6j-wave1-n80-adjudication.md
Phase 0 reads first, then adjudicate NO-EXCEPTION vs FRESH-PREREG-OK for the N≥80 near-miss (sel N 73–74). No commits.
```
