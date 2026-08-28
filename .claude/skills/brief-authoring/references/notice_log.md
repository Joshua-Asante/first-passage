# Notice — [Short observation title]

**Notice ID:** N-YYYY-MM-DD-[short-slug]
**Observed:** YYYY-MM-DD
**Author:** Joshua | claude.ai
**Source:** [live trade | backtest CSV | MC run | Notion page | conversation | other]
**Status:** `OPEN` | `GRADUATED to Q-X` | `DROPPED` | `HELD until YYYY-MM-DD`
**Lives in:** `docs/notes/notice/N-YYYY-MM-DD-slug.md` or Notion *Notice Log*

---

## §0 — Source anchor

What was the source of the observation? One file / one event / one number. Notice-phase artifacts are lightweight — §0 is one line, not a verified-commit list. The full Rule-0 burden lands on the Pre-Q if this notice graduates.

- **Source:** [specific file path, trade row, CSV cell, conversation timestamp, or live event]
- **Observed at:** [timestamp or session date]

---

## §1 — The observation

What you saw. Plain description, not interpretation. The signal in INQHIORI's I→N pass: something specific that didn't match expectation.

[1–3 sentences. Concrete, not abstract. "Guardian's May 7 exit at 11:45 produced MAE == Net P&L, which doesn't match the trailing-stop signature" — not "Guardian seems off."]

---

## §2 — Why it stands out (the N signal)

What about this observation is anomalous against the baseline? If you can't name the baseline, the observation may be noise — note that and drop.

- **Baseline:** [what the expected pattern was]
- **Delta:** [how this observation departs from baseline — magnitude, direction, mechanism]
- **Frequency check:** [is this the first instance, or have you noticed it before? If repeat, list prior notices]

---

## §3 — Candidate mechanisms (informal)

NOT pre-registered hypotheses. This section captures the first-pass thinking that might motivate a Pre-Q later. Keep it loose — the discipline of a falsifier comes at the Inquire phase, not here.

- [Mechanism A — one sentence]
- [Mechanism B — one sentence]
- [Could also be noise/coincidence — why this is plausible]

If you found yourself writing more than four candidates, you may be reaching for explanations; consider dropping back to §2 and asking whether the signal is real.

---

## §4 — Routing decision

One of:

- **GRADUATE to Pre-Q.** This observation is worth structured investigation. Open `Q-X-[slug].md` using the inquire_brief template; link this notice in §1 lineage of the Pre-Q. Reason: [why now, why this is worth the investigation cost].
- **DROP.** Logged for the record but not pursued. Reason: [too small, plausibly noise, no plausible mechanism, outside current scope, etc.].
- **HOLD until YYYY-MM-DD.** Re-check on date; graduate to Pre-Q if signal recurs OR confirms. Set calendar trigger. Reason: [need more data points before deciding; want to see if pattern repeats; etc.].

Decision: [GRADUATE | DROP | HOLD]
Reason: [one sentence]

---

## §5 — If HOLD: re-check trigger

Skip this section unless §4 = HOLD.

- **Re-check date:** YYYY-MM-DD
- **Trigger condition:** [what specific observation would graduate this on re-check — N more instances? specific magnitude? regime change?]
- **Drop trigger:** [what observation would let this be dropped — N quiet windows? mechanism falsified?]
- **Calendar entry:** [link to Calendar / Todoist event]

---

## §10 — Audit hooks

Minimal for notices; the heavy hooks live in the Pre-Q if graduated.

```bash
# If GRADUATED: confirm the Pre-Q references this notice
grep "N-YYYY-MM-DD-slug" docs/briefs/Q-*.md
# Expected: appears in §2 Prior art / lineage of the spawned Pre-Q

# If HOLD: calendar reminder check
# Re-check due: YYYY-MM-DD — verify in Calendar / Todoist
```

---

## Verification

```bash
# Canonical skill-side checker (ADR 2026-08-09) — validates notice's real §0-§4,§10 contract
$ python ~/.claude/skills/brief-authoring/scripts/check_brief.py <this-file>.md --type notice
# Expected: RESULT: well-formed

# Discipline checks (mechanical subset — repo-side declines notice, expected not a gap)
$ python scripts/check_brief.py <this-file>.md --type notice
# Expected: RESULT: NOT CHECKED — see the skill-side result above for the gate that counts
```

Notices fail by being too ceremonial. If you find yourself writing five-section observations with falsifiers, you're authoring a Pre-Q, not a notice — promote it.
