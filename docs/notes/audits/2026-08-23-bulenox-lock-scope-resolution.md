# Audit Note — Bulenox Master-account lock does not reach the simulated horizon

**Audit ID:** AUDIT-2026-08-23-bulenox-lock-scope-resolution
**Date:** 2026-08-23
**Triggered by:** external observation — Task R2 of the [§4 firm-model parallel repair
plan](../../superpowers/plans/2026-08-23-viable-strategy-parallel-s4-firm-repair.md), the named
(not opened) successor to
[`Q-FIRMEOD-1`](../../briefs/closures/Q-FIRMEOD-1-closure-falsified.md), operator-GO'd this
session
**Scope:** `core/firm_rules.py` Bulenox tiers (`Bulenox_25K/50K/100K/150K/250K`) + the
`simulate_path`/`firm_kwargs` engine path they run through
**Lives in:** `docs/notes/audits/2026-08-23-bulenox-lock-scope-resolution.md`

---

## §0 — Source anchors

- `core/firm_rules.py` — `Bulenox_25K/50K/100K/150K/250K` tier dicts, `dd_type="trailing"` rows
  now at lines 122/134/146/158/170; BluSky's two `trailing` tiers at 538/554
  (`grep -n '"dd_type": "trailing"' core/firm_rules.py` re-run at authoring time, below).
- `core/mc/simulation.py` — `simulate_path` (lines 52-198), read in full this session.
- `core/mc/preflight.py` — `firm_kwargs` (lines 84-186), read in full this session.
- `docs/briefs/closures/Q-FIRMEOD-1-closure-falsified.md` — the closure that found the lock
  language and explicitly left the scope question open (§3, §4, Iterate/entry-packet).
- Primary sources, re-fetched live this session (not read from the closure's paraphrase):
  - `https://web.archive.org/web/20260120055137/https://bulenox.com/help/master-account/`
    ("Master Account Rules" section, page footer "Updated 2/21/2023").
  - `https://web.archive.org/web/20260310032809/https://bulenox.com/help/qualification-account/`
    ("Option 1: No Scaling Account (Trailing Drawdown)" and "Option 2: EOD Account" sections,
    page footer "Updated August/14/2023").

---

## §1 — Trigger

`Q-FIRMEOD-1` (closed `FALSIFIED` 2026-08-23) found lock-adjacent language on Bulenox's Master
Account primary source — *"The trailing or EOD drawdown stops moving when the trailing or EOD
drawdown reaches the initial starting balance +100"* — but explicitly declined to resolve whether
that lock reaches the horizon this repo's engine currently simulates (Qualification-only,
absorbing-at-pass), naming the trap of assuming either answer without checking. This task is that
check.

**Failure class:** Source-of-truth fracture (candidate) — a `firm_rules.py` sourcing comment
claimed completeness ("no reset option, the only Master difference") that its own cited primary
source contradicts. Not a methodology-discipline miss; a documentation-completeness gap the prior
closure already flagged and asked a successor to close.

---

## §2 — What was verified this session (primary source, re-fetched independently)

1. **Both Wayback captures re-fetched live** (not trusted from the closure's quote) via browser
   `textContent` extraction (accordion-collapsed page; `innerText` alone under-reports — verified
   both extraction methods to confirm no additional hidden text was missed).

2. **Master Account page**, under "Master Account Rules" (Updated 2/21/2023), verbatim:
   > "The trailing rules for the Master Account are the same as for the Qualification Account,
   > except that there is no option to reset the account. The trailing or EOD drawdown stops
   > moving when the trailing or EOD drawdown reaches the initial starting balance +100."

   Confirms the closure's quote byte-for-byte. Also confirms the closure's own defect finding:
   the pre-existing `firm_rules.py` comment named only "no reset option" as "the only Master
   difference" — this page states a second, undocumented one (the lock).

3. **Qualification Account page**, read in full (not just the section the closure quoted). This
   is the new finding this task adds:
   - **Option 1: "No Scaling Account (Trailing Drawdown)"** — this is the exact geometry
     `core/firm_rules.py`'s Bulenox tiers encode (`dd_type="trailing"`, the comment at line 33-35
     cites this as "Option 1"). Its full description ("the trailing drawdown will always follow
     the current balance... if the Trader violates the allowable drawdown, the Trader's account
     is blocked... the trader can make a reset or create a new account") contains **no lock
     language anywhere** — the floor is described as tracking the peak in perpetuity, matching
     the engine's current never-locking encoding for this branch (no `dd_lock_offset_usd`
     threaded for `dd_type="trailing"`).
   - **Option 2: "EOD Account"** (a *different* drawdown mechanism Bulenox tiers do not use)
     carries the parallel lock language explicitly scoped to the post-pass stage: *"After
     Qualification, for Master Account: The EOD stops moving when the EOD reaches the initial
     balance +$100."* — the "After Qualification, for Master Account" prefix is present here
     verbatim and is the clearest textual scoping in the whole corpus.
   - Combined with the Master Account page's own text ("Master Account Rules" — a heading that,
     by construction, only describes the Master stage), **every occurrence of the +100 lock
     language across both primary-source pages is textually attached to the Master stage
     (post-Qualification promotion), never to the Qualification stage** that
     `dd_type="trailing"` models today.

4. **Engine-side check, Rule 0 (read production directly, not inferred from the tier dict)**:
   - `simulate_path` (`core/mc/simulation.py:188-196`) returns `"pass"` and **terminates the
     loop** the instant `equity >= profit_target and trade_days >= min_trading_days` — i.e., at
     exactly the "Qualification objective achieved" event. There is no code path in
     `simulate_path` that continues simulating any day after a pass, Master-stage or otherwise —
     no stage parameter exists at all.
   - `firm_kwargs` (`core/mc/preflight.py:165-186`) dispatches Bulenox's `dd_type="trailing"`
     tiers to the `trailing` branch only — `dd_lock_offset_usd` is never set for that branch
     (it's read only under `dd_type == "trailing_locking"`, i.e., Tradeify/MFFU).
   - Reproduced: `python -m pytest tests/core/test_mc_intraday_barrier.py -q` → `9 passed`;
     `python -c "import firm_rules; print(firm_rules.FIRM_RULES['Bulenox_100K'])"` confirms no
     `dd_lock_offset_usd` key present.

---

## §3 — Answer to the scope question

**No — the lock does not reach the currently-simulated horizon.** Both halves independently
confirm this, converging:

- **(a) Textual scope.** Every instance of the +100 lock language on both primary-source pages
  is attached to the Master stage (post-Qualification promotion) — the Qualification-stage
  description of the exact drawdown geometry these tiers encode (Option 1, trailing) contains no
  lock language at all.
- **(b) Structural/engine scope.** Independent of (a): `simulate_path` is absorbing at "pass" and
  never threads any post-pass stage, and `firm_kwargs` never sets `dd_lock_offset_usd` for
  `dd_type="trailing"` tiers. Even if the lock text were ambiguous about scope, there is currently
  no code path by which it could be evaluated by this engine.

Per the plan's disposition rule for this branch: the finding is recorded, and the
`firm_rules.py` sourcing comment's completeness gap is repaired (comment-only — see §5). No
`dd_type`, `trailing_dd_pct`, or other numeric field was touched. No re-classification to
`trailing_locking` is performed or proposed by this note.

---

## §5 — Repair plan

### Immediate

- [x] `core/firm_rules.py` (lines ~41-75) — sourcing comment above the Bulenox tier block
  corrected: now states both Master differences (reset option AND the +100 lock), cites the
  scope finding, and cites this note. Comment-only; `git diff --stat` (below) confirms no
  non-comment line changed.
- [x] This audit note authored as the frozen citation for the finding, per Task R2's own
  instruction (lightest artifact — one comment fix + one note, no new lab/ campaign).

### Structural

- None owed. This closes the specific completeness gap `Q-FIRMEOD-1` named; it does not open a
  new standing rule. (If a third firm's sourcing comment is later found to have the same
  "silence read as completeness" shape, that pattern crosses the two-incident bar the closure's
  own §5 flagged — watch for it, don't pre-empt it here.)

---

## §6 — Lessons to capture

- Already covered by: `Q-FIRMEOD-1`'s own §5 lesson candidate (sourcing-comment completeness,
  below the two-incident bar) — this note is the second data point on that same candidate, not a
  new lesson. No new lesson entry authored.

---

## §7 — Programme-audit signal check

- [ ] Belt-patches without independent corroboration? — No; both primary sources re-fetched live
  this session, independent of the closure's quote (per repo's own
  `lesson_verify_source_not_label`/`feedback_quotes_from_reader_summaries_are_not_quotes`).
- [ ] Belt that only grows, never prunes? — N/A.
- [ ] Falsifier thresholds drifting? — N/A.
- [ ] Methodology invoked to rationalize a decision already made? — No; the scope question was
  genuinely open going in (the closure said so), and the answer (no) was reached by reading code
  and re-fetching sources, not assumed.
- [ ] SNAG pattern? — No.
- [ ] Cross-layer contamination? — No.
- [ ] Negative heuristic crossed without repair? — No.

No escalation to programme-audit needed.

---

## §10 — Audit hooks

```bash
# Confirm the sourcing comment cites both Master differences (not just "no reset option"):
grep -n "stops moving\|starting balance +100\|no reset option" core/firm_rules.py
# Expected: comment block above Bulenox_25K names both.

# Confirm no engine-side lock hook exists for dd_type="trailing" tiers (re-verify if
# core/mc/preflight.py or core/mc/simulation.py changes):
grep -n "dd_lock_offset_usd" core/mc/preflight.py core/mc/simulation.py
# Expected: only appears under the trailing_locking branch, never trailing.

# Confirm this note is the cited successor artifact if Q-FIRMEOD-1's re-proposal bar is checked:
grep -n "AUDIT-2026-08-23-bulenox-lock-scope-resolution" core/firm_rules.py
```

---

## §11 — Closure

- **Status:** `Closed (immediate complete; structural N/A)` — 2026-08-23
- **Immediate repair completed:** 2026-08-23
- **Structural repair completed:** N/A (none owed — see §5)
- **Lessons graduated to standing rule:** none (below threshold, see §6)
- **Follow-up audits triggered:** none. Task R1 (7-tier intraday-honest re-run) and Task R3
  (survivor §4 scoring) remain separate, un-blocked-by-this-note tasks in the parent plan.

---

## Verification

```bash
$ git log -1 --format="%h %ad" --date=short -- core/firm_rules.py core/mc/simulation.py core/mc/preflight.py
$ python -c "import ast; ast.parse(open('core/firm_rules.py', encoding='utf-8').read())"
$ python -m pytest tests/core/test_mc_intraday_barrier.py -q
$ python -m pytest tests/core/ -q -k "preflight or firm"
$ grep -n '"dd_type": "trailing"' core/firm_rules.py
```
