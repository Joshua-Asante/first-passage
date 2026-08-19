# Q-PUBTRANS-1 — Did the 2026-08-14 repo-public-visibility transition actually complete cleanly?

**Status:** `OPEN — DRAFT (pre-lock)` — execution requires a separate operator GO (parent-Q convention: naming is not opening)
**Authored:** 2026-08-18
**Closed:** N/A
**Authors:** Joshua + Claude Code
**Parent question:** N/A — opened from the 2026-08-18 assumption-sweep audit note
**Sub-questions opened:** none
**Loop:** Inquire-phase Pre-Q — closure gated on three independent locational/grep reads, one of which needs an operator-held literal value and one of which needs private-archive access this session doesn't have
**Artifact path:** `docs/briefs/Q-PUBTRANS-1-public-transition-completeness.md`

---

## Section 0 — Rule 0 reads (production-source verification)

Read directly during the 2026-08-18 audit sweep and independently re-spot-checked in this authoring session (2026-08-18):

- `docs/adr/2026-08-14-repo-public-visibility-transition.md:5` — `**Status:** \`Proposed\`` — mechanical remediation (§7 Phase 1) not yet landed.
- `docs/adr/INDEX.md:109` — mirrors the identical `Proposed` status for the same ADR row.
- `docs/adr/2026-08-14-repo-public-visibility-transition.md:187-192` — residual-risk acceptance: *"a sufficiently motivated reader could partially reconstruct strategy behavior from the union of public artifacts... Residual, accepted — mitigation is out of scope for this ADR."*
- `docs/adr/2026-08-14-repo-public-visibility-transition.md:228-229` — `core/firm_rules.py:583` ruled **UNAFFECTED, explicit reason**: `_BASE_RISK` constants are load-bearing runtime values, not disclosure-only text.
- `core/firm_rules.py:583` — `_BASE_RISK = {"guardian": 0.0034, "striker": 0.0070, "aegis": 0.0150, "striker_nas100": 0.0037}`, tracked and public by design.
- `core/strategies/_archive/{aegis,guardian,nas,striker}/LOCK.md` — `## Reference backtest` and `## Locked config` headers present verbatim post-redaction, all four legs (grep-confirmed this session; the redaction replaced body text under the headers, not the headers themselves).
- `STATE.md:30-52` (OPERATOR QUEUE) — exactly 2 live items (F1 Tradeify-discharge reading; B7-REFIRE Stage 1 + M1), zero row for either the B5 safety-sweep obligation or the D9 sentinel-queue loss.
- `ops/sentinel/__main__.py:32-38` (`_prepend_run`) — writes by prepending a fresh run block ahead of the existing file content; carries no append-only guarantee across a file that has been recreated from empty.
- Commit `19beee2` (`chore(sentinel): weekly Tier-1 run 2026-08-10`) — confirmed **unreachable** from `HEAD` via `git merge-base --is-ancestor 19beee2 HEAD` (exit code 1, re-run this session).
- `docs/notes/audits/2026-08-18-strategy-generation-assumptions-sweep.md` §4 findings B5, D8, D9 and §9 audit hooks — the source of every claim and cheap-falsifier command this brief transcribes.

---

## Section 1 — Context and motivation

The 2026-08-18 assumption-sweep audit note (`docs/notes/audits/2026-08-18-strategy-generation-assumptions-sweep.md`) surfaced three unexamined assumptions clustering on one artifact: the 2026-08-14 repo-public-visibility transition. **B5** — the ADR's own `Proposed` status is treated as a trustworthy proxy for whether its Section 10 safety sweep (no live account ID / real dollar figures in the public tree or history) was actually re-run, with no STATE.md OPERATOR QUEUE row tracking the gap and the ADR's own audit-hook greps unsatisfiable by design. **D8** — the ADR accepts partial-reconstruction risk without ever measuring how partial "partial" is, while the load-bearing sizing numbers already sit in the public tree. **D9** — the sentinel queue's assumed append-only property silently dropped 11 open governance-obligation items when the history restart recreated `docs/notes/sentinel/queue.md` from empty. All three trace to the same transition event and the same failure shape: an artifact's *stated* completeness is trusted without a mechanical re-check of the record it should have produced. This connects directly to the repo's own public-clone posture doctrine (`CLAUDE.md` §Public-clone posture) and to R4 (reproducibility manifest / audit-obligation retention) in `docs/operational_rules.md` §Retention.

---

## Section 2 — Prior art / lineage

- **Audit note** `docs/notes/audits/2026-08-18-strategy-generation-assumptions-sweep.md` §4 (B5, D8, D9) — source of all three limbs; §3 D-gate deletions (5 other candidates: DD-protection/FXIFY-C2 geometry pinning, `check_pine_manifest.py` CI-detection gap, sessions-gate CI-mirror gap, sentinel Tier 2-3 cadence miss, harvest-req5 slippage constant) are unrelated surfaces already closed with citation and are explicitly **not** in scope here — none of the 5 is the open Tier-A branch-protection finding (same audit note §4 A1), which is a separate, still-open surface this Q does not touch either.
- **Transition ADR** `docs/adr/2026-08-14-repo-public-visibility-transition.md` — the artifact under audit; this brief does not re-litigate the transition decision itself, only whether its own closing conditions were met.
- **`Q-CAPBAND-1`** (`docs/briefs/Q-CAPBAND-1-cap-band-counterfactual.md`) — the structural precedent this brief follows: one combined H spanning named limbs, a single gate-criteria table, binary locational reads of already-recorded facts, no new spend.
- No prior Q has opened against this ADR's own completeness; this is the first.

---

## Section 3 — Question (Q-PUBTRANS-1)

**Q-PUBTRANS-1:** Did the 2026-08-14 repo-public-visibility transition actually complete cleanly — is its own closing condition met, and did anything get silently lost in the history restart?

(Pre-Q gate test: the question names only what's unconfirmed — a status field, a residual-risk claim never measured, a queue that may have lost items. It does not propose flipping the Status field, running a redaction sweep, or restoring queue items.)

---

## Section 4 — Falsifiable hypothesis (H-PUBTRANS)

**H-PUBTRANS**, three named limbs, one combined verdict:

- **Limb-B5 (safety-sweep completeness):** the public repo's working tree and full git history contain zero occurrences of the real account identifier, account numeric ID, or real dollar balance/fill figures the ADR's Phase 1 was supposed to have scrubbed.
- **Limb-D8 (reconstruction ceiling):** a reader restricted to the current public tree (excluding gitignored/hash-pinned Pine and Python-port files) cannot find explicit or trivially-inferable numeric values for SL type/level, TP type/level, ATR multiplier, session window, BE trigger, or trail rule for any of the four locked legs — i.e., reconstruction stays no more complete than "partial (sizing/instrument/version only)," matching what the ADR accepted.
- **Limb-D9 (queue-loss disposition):** for each of the 11 pre-transition open sentinel Action items (7 PREREG-RUNEDIT + 4 PREREG-SAMECOMMIT), some retrievable record — a private-archive commit after `19beee2`, a closure doc, a STATE.md/SESSIONS.md row, or an operator confirmation — shows it was dispositioned before the 2026-08-14 restart.

**Reject H-PUBTRANS if:** any limb fails — Limb-B5 finds ≥1 real literal in the public history, OR Limb-D8 finds ≥1 of the six fields with a concrete/trivially-inferable number, OR Limb-D9 finds even one of the 11 items with no retrievable disposition record anywhere (including private archive / operator confirmation). **Any single limb failure means the transition did not complete cleanly.**

**Accept H-PUBTRANS if:** all three limbs hold — Limb-B5 clean, Limb-D8 stays at "partial (sizing/instrument/version only)," Limb-D9 all 11 items confirmed dispositioned.

**Ambiguous-hold if:** Limb-D8 has been checked and holds, but Limb-B5 and/or Limb-D9 cannot be evaluated because their remaining step is operator-only (B5: the withheld literal values) or needs private-archive access this session lacks (D9) — the transition's completeness is **not yet knowable**, not confirmed clean.

---

## Section 5 — Forbidden moves

- **Treating "the repo is observably public with green CI for 4+ days" as proof the Section 10 safety sweep was re-run.** This is the exact substitution this Q exists to catch — observable publicness and a confirmed re-sweep are different claims, and closing the gap needs the operator-held literal values, not an inference from uptime.
- **Guessing or reconstructing the real account ID / dollar figures ourselves to run the Limb-B5 check.** These are the specific values the ADR redacted and only the operator holds; entering or deriving them under this brief would itself be the leak this Q is trying to detect. The check runs operator-side, full stop.
- **Reading D8's "sizing/instrument/version are already public by design" as evidence about SL/TP/ATR/session/BE/trail reconstructability.** The ADR's accepted residual risk is scoped to the fields already disclosed by design; whether the *other* six fields are also concretely recoverable is a different, untested claim, and conflating the two would let an already-accepted risk stand in for an unmeasured one.
- **Treating D9's already-negative greps (STATE.md, SESSIONS.md, `docs/briefs/closures/`, `git log --all` for `queue.md`) as proof the 11 items were never dispositioned.** Absence in the searched locations is not absence in the private `first-passage-archive` repo, which this session cannot reach. The correct read of a negative search here is "not found here," not "does not exist" — the same absence-in-known-location trap this repo's own lessons registry already names.
- **Editing the ADR's own Section 10 grep hooks, flipping its Status field, or backfilling the STATE.md OPERATOR QUEUE row under this brief.** All three are operator-owned changes to a ratified ADR and a capped, strictly-ordered queue; this brief only names the gap and prices the check (parent-Q convention: naming is not opening).

---

## Section 6 — Gate criteria (closure verdict)

| Verdict | Trigger condition | Disposition (typed) |
|---|---|---|
| `RESOLVED` | All three limbs individually clear: B5 clean (0 literal-value hits against full public history), D8 clean (0/6 concrete fields found in the tracked corpus), D9 clean (all 11 items have a retrievable disposition record) | `INTEGRATE` — flip the ADR's Status field, discharge the B5/D9 obligations (no STATE.md row needed — they close, not queue), record D8's residual-risk framing as measured-and-holding |
| `FALSIFIED` | Any one limb fails: B5 finds ≥1 real literal, OR D8 finds ≥1 of the six fields concretely recoverable, OR D9 finds ≥1 of the 11 items with no disposition record anywhere reachable | `STOP` for the failed limb's specific gap (re-proposal bar: a fresh remediation decision — redaction patch, doc-vocabulary sweep, or queue-loss writeup — not a re-run of this same check) — `ITERATE` for the brief as a whole, since the other limbs may still need their own verdict recorded |
| `AMBIGUOUS-HOLD` | D8 checked and clean, but B5 and/or D9's remaining step (operator-held literals; private-archive access) has not been executed | `ITERATE` — name (do not open) the operator-GO step that would resolve each still-open limb; re-test when that step runs |

**Pre-registered before any limb is read.** Per the audit's own note, the negative searches for D9 and the coarse regex pre-check for B5 are already-run facts as of 2026-08-18 (§0 of this brief and §9 of the audit note) — reusing them at closure is not amending the gate mid-investigation, since the gate's trigger conditions were fixed before this brief was authored, not adjusted to match them.

---

## Section 7 — Execution plan (self-executing, $0/K=0 — reuse the cheap-falsifier sketches supplied)

- **Phase 0 — Rule-0 reads.** Done (Section 0).
- **Phase 1 — Limb-D8, fully agent-executable ($0, ~20-30 min).** Grep the tracked (non-gitignored) corpus — `CLAUDE.md`, `core/firm_rules.py`, the 4 redacted `LOCK.md` files, `docs/methodology/`, `docs/adr/` — for `ATR|SL|TP|stop|target|session|BE|breakeven|trail`; read every hit's surrounding prose; tally per-leg which of the six fields surfaces a concrete number vs. only a generic word.
- **Phase 1 — Limb-B5, agent free pre-check + operator-only confirm.** Agent-doable now: grep full history for account-ID-shaped and dollar-figure-shaped regex patterns near `account|balance|fill|P&L` as a coarse leak-detector needing no secret input. Operator-only (~2 min): paste the withheld literal values into the ADR's own Section 10 commands, run against the public repo's full history (`git log --all -p -- . | grep -F <value>` or `git rev-list --all | xargs git grep -F <value>`); record pass/fail as a STATE.md OPERATOR QUEUE row and flip the ADR Status accordingly.
- **Phase 1 — Limb-D9, already run negative + one remaining private-archive/operator step.** Already executed this session (§0): `git log --all` for `docs/notes/sentinel/queue.md`, `git merge-base --is-ancestor 19beee2 HEAD` (confirmed unreachable), and greps of `STATE.md`/`docs/SESSIONS.md`/`docs/briefs/closures/` for the 11 item-ID stems (`PREREG-RUNEDIT-*`, `PREREG-SAMECOMMIT-*`) — all negative. Remaining $0 step needs private `first-passage-archive` repo access this session doesn't have: `git log -p` for `docs/notes/sentinel/queue.md` on any post-2026-08-10 commit mentioning those 11 IDs, or simply asking the operator whether the 11 open items from the 08-10 sentinel run were ever closed before the 08-14 transition.
- **Phase 2 — Verdict assertion.** Apply Section 6 mechanically per limb, then combine per Section 4's Reject/Accept/Ambiguous-hold rule.

---

## Section 8 — Verdict pre-registration

§4 above **is** the frozen decision rule — fixed in this draft (2026-08-18) before any limb is read, the same guarantee Section 6's note states explicitly. No separate pre-registration file is needed beyond it. What's owed at operator GO is committing/ratifying this draft itself before Phase 1 executes (this Q is named, not opened).

---

## Section 9 — Closure record format

Per `references/closure_record.md`, with the mandatory typed `## Iterate` block. `RESOLVED` → `docs/briefs/closures/Q-PUBTRANS-1-closure-resolved.md`; `FALSIFIED` → `…-closure-falsified.md`; `AMBIGUOUS-HOLD` → `…-closure-ambiguous-hold.md` naming which limb(s) remain unresolved and what operator/private-archive step would resolve them.

---

## Section 10 — Audit hooks (runnable)

```bash
# --- Limb-B5: safety-sweep completeness ---
# Agent-doable free pre-check (coarse leak-detector, no secret input needed):
git log --all -p | grep -EiC1 "(account[_ -]?(id|number)|balance|fill|P&L)[^\n]{0,40}[0-9]{4,}"

# Operator-only (~2 min, needs the withheld literal values):
# git log --all -p -- . | grep -F "<real account identifier>"
# git log --all -p -- . | grep -F "<real dollar figure>"
# git rev-list --all | xargs git grep -F "<literal>"

# --- Limb-D8: reconstruction ceiling ---
grep -rniE "ATR|\bSL\b|\bTP\b|stop|target|session|\bBE\b|breakeven|trail" \
  CLAUDE.md core/firm_rules.py core/strategies/_archive/*/LOCK.md docs/methodology/ docs/adr/

# --- Limb-D9: sentinel queue-loss disposition ---
git log --all -- docs/notes/sentinel/queue.md
git merge-base --is-ancestor 19beee2 HEAD; echo "exit=$?"   # expect 1 (unreachable)
grep -n "PREREG-RUNEDIT-\|PREREG-SAMECOMMIT-" STATE.md docs/SESSIONS.md docs/briefs/closures/*.md
# Remaining step (private archive, not runnable here):
# git -C <first-passage-archive-clone> log -p --since=2026-08-10 -- docs/notes/sentinel/queue.md
```

---

## Verification

```bash
# Discipline checks (mechanical)
$ python scripts/check_brief.py docs/briefs/Q-PUBTRANS-1-public-transition-completeness.md --type inquire

# Production-source verification (Section 0 anchor confirmation)
$ grep -n "^\*\*Status" docs/adr/2026-08-14-repo-public-visibility-transition.md
$ sed -n '109p' docs/adr/INDEX.md
$ sed -n '30,52p' STATE.md   # confirm 2 items, no B5/D9 row
$ grep -rn "Locked config\|Reference backtest" core/strategies/_archive/*/LOCK.md
$ git merge-base --is-ancestor 19beee2 HEAD; echo "exit=$?"   # expect 1

# Cross-reference verification (audit note grounding)
$ grep -n "B5\.\|D8\.\|D9\." docs/notes/audits/2026-08-18-strategy-generation-assumptions-sweep.md
```

If any verification command fails, the brief is not complete. Re-author the section that broke; do not handwave.

---

## Pre-Lock Checklist (DRAFT briefs only)

- [x] Section 0 paths read with anchors
- [x] Section 3 passes the symptom-only rephrase
- [x] Section 4 hypothesis binary
- [x] Section 5 forbidden moves genuinely tempting
- [x] Section 6 triggers specific
- [x] Section 8 pre-registration owed at operator GO
- [x] Section 10 hooks runnable
- [ ] Operator GO owed before Phase 1 — this brief is named, not opened
