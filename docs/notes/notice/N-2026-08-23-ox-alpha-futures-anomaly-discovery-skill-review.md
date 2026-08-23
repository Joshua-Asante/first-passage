# Notice — Ox-alpha review of `futures-anomaly-discovery`: most objections miss or restated withdrawn doctrine; five skill-text skews survive

**Notice ID:** N-2026-08-23-ox-alpha-futures-anomaly-discovery-skill-review
**Observed:** 2026-08-23
**Author:** Cursor Cloud Agent (commission: send a sanitized copy of the skill to `stealth/ox-alpha` via `$OPEN_ROUTER_API`, ask how to improve it for our purposes, reconcile every objection against the real skill before treating any as a finding)
**Source:** OpenRouter `stealth/ox-alpha` chat-completions, two calls (both `finish=length` in the reasoning channel; content field empty). Reconciled against the real skill and its owners, not against the sanitized excerpt.
**Status:** `OPEN` — routed `DROP` as an Inquire-phase question (no new Q). Repairs landed 2026-08-23 against [`2026-08-23-futures-anomaly-discovery-skill-skew-implementation.md`](../../superpowers/plans/2026-08-23-futures-anomaly-discovery-skill-skew-implementation.md) (`GO 2026-08-23`). Skill now points at the harvest / admission / deep-lane owners. Still DROP as a Q.
**Lives in:** `docs/notes/notice/N-2026-08-23-ox-alpha-futures-anomaly-discovery-skill-review.md`

Lane: [`2026-08-22-ox-alpha-adversarial-lens-scope.md`](../../adr/2026-08-22-ox-alpha-adversarial-lens-scope.md) (use 2 of the sanctioned lens; DL-2 prereg was use 1). Zero authority; objections are not findings until the table below.

---

## §0 — Source anchor

- **Source:** sanitized skill copy sent to `stealth/ox-alpha` (genericized SKILL.md + tool-discipline; no names, dates, proprietary numbers, or fingerprintable filters). Real-skill reconciliation against `.claude/skills/futures-anomaly-discovery/SKILL.md` + `reference/tool-discipline.md` @ `b2e5f15` (2026-08-22), `docs/methodology/strategy_harvest.md`, `docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md`, `lab/discovery/register_search.py`, `lab/discovery/admission_schema.py`.
- **Observed at:** 2026-08-23. Two API calls, model id `stealth/ox-alpha`, `$0` (`usage.cost = 0`). Call 1: 4914 prompt / 8000 completion tokens, all reasoning. Call 2 (lists-only prompt): 4673 / 6000, same. The numbered O/E draft in call 1's reasoning is the review body used below.

---

## §1 — The observation

A sanitized copy of the discovery skill was sent with a genericized "our purposes" brief (trial-count is the binding constraint; published-mechanism confirmation is the fundable route; agents execute so mechanical gates beat exhortation; discovery never blesses; same-units cost attestation; claim-family-specific nulls). Ox-alpha produced ~18 numbered objections plus ranked edits, all in the reasoning channel. Reconciled against the real skill and its owners, five items survive as skill-text skews; the rest are already discharged, wrong-layer, or prompt artifacts.

---

## §2 — Why it stands out (the N signal)

- **Baseline:** the lens's own ADR — every objection is candidate input until checked against the unsanitized artifact. DL-2 use 1 already showed this mix (real hits + already-discharged + sanitization artifacts).
- **Delta:** the highest-leverage cluster (family search-budget as a kill; admission-requirement restatement) is not a new idea from the model — it is the skill silently restating withdrawn harvest doctrine. The model independently aimed at that cluster from the sanitized text.
- **Frequency check:** second production use of the lane. Revert trigger (b) (three consecutive zero-value uses) does not tick — several objections survived reconciliation.

---

## §3 — Reconciliation (not findings until this table)

Ox-alpha's drafted objections, checked against the real skill / code / harvest owner. Verdicts: **SURVIVES** (finding) · **PARTIAL** · **DISCHARGED** · **ARTIFACT** (created by sanitization or the purposes brief, not by the skill).

| ID | Ox-alpha claim (compressed) | Against the real artifact | Verdict |
|---|---|---|---|
| O1 | Prereg widening-void is exhortation: `--prereg` checks exists / `.md` / non-empty / in-repo only | Skill L105–110 states this exactly. `register_search._require_prereg` matches. Deep lane hash-pins `grammar.json`, not the mechanism-first prereg body. Accurate description of current machinery; a hash-pin would be new work, not a skill lie | PARTIAL — true; not a skill defect. Candidate improvement, code-sized |
| O2 | Blind lane is cheaper than the default and poisons the shared K ledger that kills harvest seeds | Blind *is* cheaper (legacy 11-key, prereg omittable) — intended. "Must stay expensive" was in the purposes brief, not the skill (`_require_prereg` calls unbound blind "a known residual, not an oversight"). Shared-ledger *kill* assumes family K-bank is still a gate. Owner [`2026-08-04-family-k-bank-disclosure-not-gate.md`](../../adr/2026-08-04-family-k-bank-disclosure-not-gate.md) withdrew that. Skill L62–64 still says a burned family "kills the seed regardless of quality" | SURVIVES — skill restates withdrawn Req-3 |
| O3 | Refuse-at-open writes no refusal ledger; iterate-until-pass is invisible | Code `sys.exit`s with no manifest. Skill describes this accurately. A refusal ledger is new machinery | PARTIAL — true of the code; skill is not wrong |
| O4 | Pre-admission N-EDGE (net expectancy / CI / DSR) is an uncounted in-house peek | Harvest Req-2 wants those numbers cohort-cited, not sneak-peeked. Computing them from a look is already a Rule-1 violation. Not a missing skill clause | DISCHARGED |
| O5 | Pipeline "clears the crude multiplicity floor" vs "verdict is always a hand-off" | `close()` both names Bonferroni-killed candidates *and* says "first-pass only → hand to strategy-validation". Wording collision ("promoted to hypothesis" vs "never a promotion") is real agent-misread risk | SURVIVES — wording |
| O6 | Null-validity citation is textual; a wrong-family doc would pass | Red-flag is prose-only. No family-taxonomy registry lives in the skill. Exhortation, same class as O1 | PARTIAL — true; improvement is a registry, not a sentence |
| O7 | Random restarts / seeds (symbolic regression, HMM inits) uncounted in K | `reference/tool-discipline.md` bounds operator set / complexity / population·generation, not restart count | SURVIVES — tool-discipline gap |
| O8 | Daily-loss / trailing-DD constraints absent | TNEC N-EDGE is in the skill (L94–99). Daily-loss / trailing-DD live in `firm_rules` / `strategy-validation`. Discovery restating them would be the layer leak the skill's wall forbids | DISCHARGED — wrong layer |
| O9 | Numeric threshold for "large" family K missing | Sanitization replaced the skill's `GC/MGC` example with "large". Real skill still *kills* on a burned family. Owner says disclosure-not-gate | SURVIVES — same cluster as O2 |
| O10 | Admission-file schema unspecified; agents cannot build `admission.json` from the skill | `lab/discovery/admission_schema.py` is the owner. Skill names flags, not the module | SURVIVES — missing pointer |
| O11 | Hygiene gaps: roll/splice DoF, limit-locked sessions | Tool-discipline already covers vol-U, bid-ask bounce, back-adjustment, and hands session/clock to `databento-data` | PARTIAL — incremental; not a hole in the stated split |
| O12 | Orphan `open` without `close` has no expiry | Manifests persist; `status` lists them. No auto-expire | PARTIAL — true; new machinery |
| O13 | No cross-agent candidate fingerprint / dedup | Profile consult *is* the instrument × mechanism-class dedup. Feature-level fingerprinting is new scope | PARTIAL — consult exists; action-on-hit is O15 |
| O14 | Effect-size units unconstrained; same-units only covers cost-law | Harvest Req-2 is per-instrument δ/σ. Owner has five requirements; skill still lists four and treats same-units as a sidecar | SURVIVES — skill/harvest drift (four vs five) |
| O15 | Profile consult: action when the cell is bound is unstated | Skill requires `--profile-consult`. `instrument_profiles.py cell` is BLOCKING on `DEAD`. Skill never says "nonzero consult ⇒ address in the prereg or do not open" | SURVIVES — missing action-on-hit |
| O16 | "Mining without a mechanism is fine" vs mechanism-first default | Different lanes. Harvest / mechanism-first require grounding; `--lane blind` is the mechanism-free escape. Fine ≠ fundable | DISCHARGED |
| O17 | Runner order `mine → bind-K → score` vs declare-before-look | Skill already says synthetic-only until an operator authorizes a real `open` / pull. Peek-before-open is exhortation for any pre-reg | PARTIAL — sequence prose is messy; enforcement matches the skill's claim |
| O18 | Admission requirements duplicated here and in the harvest owner → drift | Drift has already happened: skill has four reqs + burned-family kill; owner has five and disclosure-only Req-3 | SURVIVES — same cluster as O2 / O14 |

Reconciliation-side (not in the ox-alpha list; found while checking the real module):

- Skill documents `--lane blind` and mechanism-first only. `register_search.py` also implements `--lane deep` (charter 2026-08-16). Agents following the skill alone will not find the live second lane.
- Skill says blind has "no admission gate". Code: `--admission-file` is optional on blind, and if supplied still refuses.

Prompt artifacts (do not treat as findings): "blind must stay expensive" (purposes brief); "large" as the family-bank threshold (sanitization of `GC/MGC`); prop-firm daily-loss as a discovery-skill hole (O8).

---

## §4 — Routing decision

**DROP** as an Inquire-phase question. Reason: nothing here needs a new Q — the surviving cluster is the skill restating owners that already moved (`strategy_harvest.md` Req-3/5, `register_search` deep lane, `admission_schema.py`). Applied 2026-08-23 as skill-text repairs specified in [`2026-08-23-futures-anomaly-discovery-skill-skew-implementation.md`](../../superpowers/plans/2026-08-23-futures-anomaly-discovery-skill-skew-implementation.md); do not open a Pre-Q to re-decide ratified harvest doctrine. The skill now points at those owners.

Surviving findings, ranked by agent-harm if left stale (applied 2026-08-23):

1. **Req-3 text is withdrawn doctrine.** Skill L62–64 still kills on a burned family. Owner ADR 2026-08-04: mandatory disclosure, cannot fail a seed. Same cluster: O2, O9, O18.
2. **Admission list is a stale subset.** Skill says four requirements; harvest owner has five (same-units / cost-law is Req-5, not a sidecar). Pointer-only repair: name the owner, stop restating the list.
3. **Missing pointers / actions the code already has.** Point at `lab/discovery/admission_schema.py` (O10). State bound-cell action (O15). Name `--lane deep` (reconciliation-side).
4. **Wording.** "Clears the crude floor" vs "always a hand-off" / "promoted to hypothesis" vs "never a promotion" (O5).
5. **Tool-discipline increment.** Count restart / seed attempts in declared K (O7).

Not findings (already true, wrong layer, or new machinery): O1 widening hash-pin, O3 refusal ledger, O4 peek N-EDGE, O6 family registry, O8 account constraints, O11 extra hygiene, O12 orphan expiry, O13 feature fingerprint, O16 mechanism-free vs default, O17 peek-before-open.

---

## §5 — If HOLD: re-check trigger

Skipped (`§4 = DROP`).

---

## §10 — Audit hooks

```bash
# Finding 1 gone from the skill; harvest owner remains the list
grep -n "kills the seed regardless of quality" .claude/skills/futures-anomaly-discovery/SKILL.md
# Expected after GO: empty.

# Finding 2: no restated four-req list in the skill
grep -n "four admission" .claude/skills/futures-anomaly-discovery/SKILL.md
# Expected after GO: empty; pointer at strategy_harvest.md only.

# Deep lane named
grep -n "lane deep" .claude/skills/futures-anomaly-discovery/SKILL.md
grep -n 'choices=\[\"blind\"' lab/discovery/register_search.py

# This notice is the owner for the review; ADR addendum points here
grep -n "N-2026-08-23-ox-alpha-futures-anomaly-discovery-skill-review" \
  docs/adr/2026-08-22-ox-alpha-adversarial-lens-scope.md

# Plan no longer PENDING
grep -n "AUTHORIZATION: GO 2026-08-23" \
  docs/superpowers/plans/2026-08-23-futures-anomaly-discovery-skill-skew-implementation.md
# Expected after GO: a hit.
```

---

## Addendum 2026-08-23 — repairs specified, PENDING GO

Work order: [`2026-08-23-futures-anomaly-discovery-skill-skew-implementation.md`](../../superpowers/plans/2026-08-23-futures-anomaly-discovery-skill-skew-implementation.md). Header is `PENDING OPERATOR GO`. This notice stays `DROP` as a Q. The skill is still unedited. After that GO, the plan’s Task 4 writes the “repairs landed” line here.

---

## Addendum 2026-08-23 — repairs landed (GO executed)

Operator GO on the plan. Tasks 1–3 landed: skill harvest intake is pointer-only (five requirements; Req-3 disclosure-not-gate); `--admission-file` points at `lab/discovery/admission_schema.py`; bound-cell BLOCKING action named; `--lane deep` stub present; tool-discipline uses “routed as” and counts restart/seed K; harvest §2 token is “five”. Status stays `DROP` as a Q. No new ADR.

---

## Verification

```
$ python scripts/check_brief.py docs/notes/notice/N-2026-08-23-ox-alpha-futures-anomaly-discovery-skill-review.md --type notice
# Expected: type=notice is unmodeled (type-agnostic checks only); no HARD on a notice.

$ grep -n "kills the seed regardless of quality" .claude/skills/futures-anomaly-discovery/SKILL.md
# Expected after GO: empty

$ grep -n "four admission" .claude/skills/futures-anomaly-discovery/SKILL.md
# Expected after GO: empty

$ grep -n "AUTHORIZATION: GO 2026-08-23" docs/superpowers/plans/2026-08-23-futures-anomaly-discovery-skill-skew-implementation.md
# Expected: a hit
```
