# Pre-registration — Aegis→6J prop reconstruction **v2.1** (degeneracy tie-break; closes v2 Stage-1 AMBIGUOUS → RESOLVED c05)

**Status:** `FROZEN` (operator §9 signed 2026-07-16 / JA — approved in-session). Stage-1
**RESOLVED → winner c05**; Stage-2 solo Part A authorized. No in-place amendment (Trap #12).
**Role:** the **fresh pre-reg the v2 §6 AMBIGUOUS branch requires** — adds **one** pre-declared
tie-break and closes the v2 Stage-1 selection with a single winner. Does **not** amend the
v2 pre-reg (`FROZEN`) or its AMBIGUOUS Stage-1 record (Known Trap #12 — no in-place edit); this
is the sanctioned close-and-reopen route for a mechanical-rule non-discrimination.
**Parent (unchanged):** v2 window-realigned pre-reg
[`2026-07-16-aegis-6j-prop-reconstruction-v2-window-realigned-prereg.md`](2026-07-16-aegis-6j-prop-reconstruction-v2-window-realigned-prereg.md)
(`FROZEN` §9 2026-07-16 / JA). **Inherits v2 §2.1–§2.5, §2.7 byte-identical**; the **only**
change is a tie-break addendum to §2.6 (below). Windows, cells, mechanism, engine unchanged.
**Grandparent:** v1 `CLOSED — Stage-1 FALSIFIED`; v2 resolved that (N≥80 reachable).
**Candidate class / Aegis declaration / gate of record:** unchanged from v2 (Class S; Aegis-bearing
solo 6J; survivor gate `2026-07-13-prop-survivor-scoring-prereg.md`).
**Loop of record:** STRATEGIC.
**Authored:** 2026-07-16 · Claude Code (operator-directed: adjudicate AMBIGUOUS → tie-break closure).

---

## §0 — Rule-0 reads (verified this session 2026-07-16, byte-exact)

- **`docs/briefs/pre-registration/2026-07-16-aegis-6j-prop-reconstruction-v2-window-realigned-prereg.md`**
  (v2, FROZEN) — §2.6 selection rule (max mean qty; tie-break lower sel maxDD → higher sel net;
  two-cell tie on all keys ⇒ AMBIGUOUS, §6); §2.3 degeneracy collapse (c05≡c06 / c02≡c04 /
  c11≡c12; 9 unique panels); §2.7 Stage-2 solo Part A.
- **`lab/analysis/aegis/aegis_6j_prop_reconstruction_2026-07/wave1_v2_metrics.json`** +
  **`lab/analysis/aegis/aegis_6j_prop_reconstruction_2026-07/SWEEP_LOG_v2_table.md`** (driver
  `lab/analysis/aegis/aegis_6j_prop_reconstruction_2026-07/wave1_reslice_v2.py`, validated 12/12 vs
  v1 pins; hash-gated) — **12/12 clear (a)–(e)**; **max mean qty = 4.60, held by c05 AND c06**,
  which are **byte-identical** (both sha `ED91CD2D5D40`): sel maxDD 1.2425, sel net $8,803, ho
  net $5,755 — identical on every key. c11/c12 next at 4.5684 (strictly lower; not tied at top).
  Mechanical §2.6 → **AMBIGUOUS**.
- **`lab/analysis/aegis/aegis_6j_prop_reconstruction_2026-07/WAVE1_SHA256SUMS`** — confirms
  `c05_…_ed91cd2d.csv` and `c06_…_ed91cd2d.csv` share one digest (the 0.55% risk-display
  saturated to the 0.40% cap-8 qty profile; operator-confirmed).
- **`CLAUDE.md:55`** (Multiplier System) — standing doctrine: *"Always rounded down (never round
  up on risk)."* This is the tie-break's ground (below), **not** a performance metric.

---

## §1 — Context

v2 Stage-1 ran as a pure offline re-slice of the 9 pinned panels on the realigned windows.
Every substantive filter passed and (d) N≥80 was reachable — **12/12 cells cleared (a)–(e)**.
The max-mean-qty selection resolved to a **two-cell tie: c05 and c06**, which are **the same
CSV** (`ED91CD2D`; the c05≡c06 degeneracy pre-disclosed in v2 §2.3). They tie on mean qty **and**
both existing tie-breaks *because they are byte-identical* — so the mechanical rule returned
**AMBIGUOUS** (v2 §6).

This is **not** a discrimination failure between two distinct candidates; it is a **label**
ambiguity inside a byte-identical degeneracy. The winning *panel* is unambiguous
(`ED91CD2D`, cap8 / 16:00 fill); only the `risk_pct_display` label (0.40% vs 0.55%) is
undetermined. Per v2 §6 the resolution is a **fresh pre-reg adding one pre-declared tie-break**
(no in-place edit; no post-hoc performance metric). This is that pre-reg.

---

## §2 — Frozen protocol

**§2.1–§2.5, §2.7 inherit the v2 pre-reg byte-identical.** Windows (sel 2022-01-12→2025-06-30 /
holdout 2025-07-01→2026-06-30 / Stage-2 panel 2022-01-12→2026-06-30), the 12-cell grid, the
mechanism, the degeneracy collapse, and the Stage-2 solo Part A engine are **unchanged**.

### §2.6′ — Selection rule + **degeneracy tie-break** (the ONLY delta vs v2)

Unchanged: among survivors select **max mean position quantity**; tie-break **lower sel maxDD →
higher sel net $**.

**New (pre-declared) — degeneracy tie-break, applied last:** if the cells resolving to the top
after the above are **byte-identical** (same CSV `sha256`), they are the **same panel** under
different labels. Collapse them to their one unique panel and, for the display label only,
select the **lower `risk_pct_display`** — consistent with the standing **"never round up on
risk"** doctrine (`CLAUDE.md:55`).

**Why this is legitimate (not post-hoc gaming):** the tied cells are byte-identical, so **no
tie-break of any kind can favor one on performance** — PF, expectancy, net, maxDD are all equal.
The tie-break therefore touches **only** the display label, is **performance-agnostic**, and is
grounded in existing doctrine rather than the observed result. The **deployable panel handed to
Stage-2 is identical** regardless of the label chosen. (Contrast: a tie-break that used PF or
expectancy to choose between *distinct* cells would be the forbidden post-hoc metric — §5.)

**If the top tie were between NON-identical cells:** this tie-break does **not** apply — that
remains AMBIGUOUS and needs its own fresh pre-reg. (Not the case here.)

---

## §3 — Calibration / discrimination note

No new cells, no new window, no new K — the v2 12-cell re-slice is reused verbatim. The tie-break
adds discrimination for the byte-identical-degeneracy case only. No ceiling move; no
holdout-as-selector.

---

## §4 — Falsifier (H)

**H-TIEBREAK-v2.1:** applying §2.6′ to the v2 run yields **exactly one** winner. Since the top
tie is byte-identical (c05≡c06, sha `ED91CD2D`), the degeneracy tie-break resolves it
deterministically to the **lower risk label → c05 (cap8 / 0.40% / 16:00)**; deployable panel
`ED91CD2D`.

**Falsified / close:** H-TIEBREAK-v2.1 is **falsified** if §2.6′ does **not** yield exactly one
winner — i.e., the top tie is between **non-identical** cells (different sha), so the
byte-identical precondition fails and the degeneracy collapse does not apply. Then close
AMBIGUOUS and open another fresh pre-reg with a distinct pre-declared tie-break. (Not the case
here: c05≡c06 share sha `ED91CD2D`, so the falsifier does not fire.)

**H-SOLO (unchanged, still open):** the winner's panel alone clears Part A (bust ≤ 3.0% +
P(pass) ≥ 50%, Run-2) on **both** `Tradeify_Select_100K` and `MFFU_Rapid_100K`. Not claimed here;
Stage-2 FALSIFIED would close the winner expression (no compose, no in-place reweight).

---

## §5 — Forbidden moves

- **Using a performance metric (PF / expectancy / net / maxDD) to break the tie.** The cells are
  byte-identical — any such "discriminator" is noise-free-equal and its use would be a post-hoc
  metric dressed as a tie-break (v2 §6 "no post-hoc metric").
- **Selecting the HIGHER `risk_pct_display`** (0.55%) — violates never-round-up-on-risk, and
  buys nothing (same panel).
- **Treating the byte-identical panels as distinct candidates** (double-counting K, or claiming
  0.55% is a separately-validated config).
- **Amending v2 in place** to insert the tie-break (Trap #12) — this fresh pre-reg is the route.
- **Carrying the label choice into Stage-2 as if it changed the panel** — the Stage-2 CSV is
  `ED91CD2D` either way; only the documented Pine `risk_pct_display` input differs.
- **Reading `compute_default_config()['bust_rate']`** for Stage-2 Part A (v2 §5 carries).

---

## §6 — Gate criteria (binary)

### Stage 1-v2.1 (tie-break application)

| Verdict | Trigger | Disposition |
|---|---|---|
| **RESOLVED** | §2.6′ yields exactly one winner | Pin winner + proceed to Stage-2 solo Part A (v2 §2.7) |
| **AMBIGUOUS** | Top tie is between **non-identical** cells (different sha) | Close; another fresh pre-reg with a distinct pre-declared tie-break |

**Applying §2.6′ to the v2 run ⇒ RESOLVED. Winner = c05:** `max_contracts` 8 · `risk_pct_display`
**0.40%** · `eod_fill_deadline_et` 16:00 (`pine_eod_trigger_et` 15:45) · panel sha `ED91CD2D5D40`
· sel N 95 · sel maxDD 1.24% · sel meanQ 4.60 · sel net $8,803 · ho net $5,755 · envelope-YES
(overnight 0%, fills ≤ 16:00). *Pending §9 signature.*

### Stage 2 (solo Part A) — inherits v2 §2.7 / §6 verbatim (unchanged, still to run).

---

## §7 — Prior-look disclosure (complete at freeze)

Inherits v2 §7 (all 12 cells + v1 FALSIFIED close + reachability recompute + H1-2025 shift), **plus:**

| # | Date | Artifact | Note |
|---|---|---|---|
| v2 | 07-16 | v2 Stage-1 run | **12/12 clear (a)–(e)**; max mean qty 4.60 tied c05≡c06 (sha `ED91CD2D`); mechanical §2.6 → **AMBIGUOUS** |
| tb | 07-16 | This tie-break | authored **after** seeing AMBIGUOUS (as v2 §6 requires); tied cells **byte-identical** ⇒ tie-break cannot favor on any performance metric; resolves **label only**, grounded in `CLAUDE.md:55`; Stage-2 panel identical regardless |

Honesty anchor: the tie-break is admissible precisely **because** the tied cells are byte-identical
— there is no performance degree of freedom to exploit. Full transparency that it was authored
post-AMBIGUOUS is disclosed here.

---

## §8 — Run protocol

No new computation. The v2 run (`wave1_v2_metrics.json`, hash-gated) is the input.

1. §9 signed.
2. Apply §2.6′ to the pinned v2 metrics → winner **c05** (deterministic; §6).
3. Pin winner Pine inputs (`max_contracts=8`, `risk_pct_display=0.40`, `pine_eod_trigger_et=15:45`)
   + winner CSV sha256 `ED91CD2D5D40` + `DEPLOYABLE-DEFAULT-ENVELOPE: YES`.
4. Proceed to Stage-2 solo Part A under v2 §2.7 (separate scoring session; H-SOLO still open).

---

## §9 — Operator signature (the tie-break freeze + Stage-1 resolution)

```
SIGNED / FROZEN: 2026-07-16 / JA          (operator-approved in-session)
Accept the §2.6′ degeneracy tie-break (byte-identical top tie → lower risk_pct_display,
never-round-up-on-risk). Resolves v2 Stage-1 to winner c05 (cap8 / 0.40% / 16:00 / ED91CD2D).
Authorizes Stage-2 solo Part A on that panel. No Stage-2 G4 cell before this block is filled.
```

---

## §10 — Audit hooks (runnable)

```bash
# 1. Signature before Stage-2
grep -n "SIGNED / FROZEN:" docs/briefs/pre-registration/2026-07-16-aegis-6j-prop-reconstruction-v2.1-tiebreak-prereg.md

# 2. Top tie IS byte-identical (tie-break precondition holds)
python -c "import json; m=json.load(open('lab/analysis/aegis/aegis_6j_prop_reconstruction_2026-07/wave1_v2_metrics.json')); t=max(r['sel_mean_qty'] for r in m); tied=[r for r in m if abs(r['sel_mean_qty']-t)<1e-9]; print('tied:', [(r['cell'],r['risk']) for r in tied]); print('one sha:', len({r['sha'] for r in tied})==1)"
# expect: tied c05(0.40)/c06(0.55); one sha: True

# 3. Winner is the LOWER risk label (never-round-up)
grep -n "Winner = c05\|risk_pct_display\*\* 0.40\|0.40%" docs/briefs/pre-registration/2026-07-16-aegis-6j-prop-reconstruction-v2.1-tiebreak-prereg.md

# 4. Tie-break is label-only / performance-agnostic (no post-hoc metric)
grep -n "performance-agnostic\|byte-identical\|no post-hoc metric\|never round up" docs/briefs/pre-registration/2026-07-16-aegis-6j-prop-reconstruction-v2.1-tiebreak-prereg.md

# 5. Does not amend v2 (Trap #12)
grep -n "does \*\*not\*\* amend\|Known Trap #12\|fresh pre-reg" docs/briefs/pre-registration/2026-07-16-aegis-6j-prop-reconstruction-v2.1-tiebreak-prereg.md
```

---

## Verification

```bash
PYTHONIOENCODING=utf-8 python scripts/check_brief.py \
  docs/briefs/pre-registration/2026-07-16-aegis-6j-prop-reconstruction-v2.1-tiebreak-prereg.md --type brief
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-16 | Authored PROPOSED — v2.1 degeneracy tie-break (byte-identical top tie → lower risk label, never-round-up-on-risk); closes v2 Stage-1 AMBIGUOUS → RESOLVED c05 (cap8/0.40%/16:00/ED91CD2D) | Claude Code (operator-directed) |
| 2026-07-16 | §9 signed → `FROZEN`; Stage-1 RESOLVED → c05; Stage-2 solo Part A authorized | JA (operator, in-session) + Claude Code |
