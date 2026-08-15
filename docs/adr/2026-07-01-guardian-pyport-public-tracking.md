# ADR 2026-07-01 — Guardian Python port was publicly tracked: assessment + untracking

**Status:** `Accepted`
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** `2026-08-14-repo-public-visibility-transition.md` — "repo stays private" premise + §2.6 Forward question (resolved toward redaction); §2 untracking decision unaffected
**Retain-until:** none
**Decision date:** 2026-07-01
**Authors:** Joshua + Claude Code
**Related:** ADR `2026-06-23-tv-backtest-egress-automation.md` (commissioned the port; its §2/§5 edge-protection reasoning walled off the live TV *account* and third-party *Pine uploads* but never weighed public tracking of the port artifact itself); `lab/analysis/legacy/tom_spx/PINE_MANIFEST.sha256` (the hash-pin-for-untracked-source precedent, and the 2026-06-16 local-copy-loss anchor); CLAUDE.md §Public-clone posture; ADR `2026-05-10-manifest-integrity-gate.md` (M-9: a manifest without a gate drifts)
**Layer:** governance / public-clone posture

---

## §0 — Rule 0 reads (production-source verification)

Files read **before** authoring this ADR, all at commit `dc07898` (HEAD of `main` via merge #256) on 2026-07-01:

- `lab/analysis/legacy/guardian_parity_2026-06-23/guardian_signal.py` — the disclosure object. Verbatim contents confirmed: full `GUARDIAN_V55_CONFIG` dict (all locked signal-layer constants incl. hour-block flags and day filter), Pine-faithful `_ema`/`_rma`/`_atr` seeding, session/H12-latch/recovery-cross logic, and a docstring naming grace-stop semantics, `process_orders_on_close=false`, `slippage=3`, and Pine line numbers.
- `lab/analysis/legacy/guardian_parity_2026-06-23/test_guardian_signal.py`, `README.md`, `run_parity.py` — tests restate locked filter semantics in assertions; README publishes the parameter one-liner, the execution-gap table with locked values, and the RESOLVED-POSITIVE parity verdict (net 0.46% / PF 1.76% over the full 52-trade window); `run_parity.py` embeds `GUARDIAN_EXEC` (slippage 3 ticks, mintick 0.01, grace 1b/2.0×).
- `.gitignore` — `**/*.pine` block + the two narrow `.pine` exceptions (tom_spx 2026-06-16, pine_check fixtures 2026-06-23); no entry covered Python ports before this ADR.
- `core/strategies/guardian/LOCK.md` — tracked + public at authoring time; its "Locked config (transcribed from strategy file header)" block published the full entry/exit parameter set. *(2026-08-14: this block was itself redacted — see the change-history row below — so the values are not repeated here.)*
- Prior tracked disclosures confirmed by direct read/grep at `dc07898`: `lab/archive/oanda_stage1/guardian_stage1.py` (a prior committed Python implementation of the same signal predicates, frozen-historical), `lab/codification/primitives.py` (Guardian's `recoveryLong` construction quoted verbatim, `emaSlowLen` default 385), `lab/analysis/legacy/guardian_filter_sweep_2026-06-20/README.md` (full filter enumeration citing the Pine), `docs/superpowers/specs/2026-06-28-pine-mql5-ea-conversion-design.md` line 63 (full Guardian parameter row + "Path-E `NextOpenEngine` reproduces it").
- Git history: `git log --follow` on `guardian_signal.py` — public since 2026-06-23 (first commit `d9e8dd8`, latest content at `dc07898`). Repo is public; no tags/rewrites affecting the path.

---

## §1 — Context

The public-clone posture (CLAUDE.md; .gitignore) holds **Pine strategy source (`**/*.pine`) privately "to protect the live edge,"** hash-pinned via `core/strategies/MANIFEST.sha256`. On 2026-06-23, ADR `2026-06-23-tv-backtest-egress-automation.md` Path E landed `lab/analysis/legacy/guardian_parity_2026-06-23/guardian_signal.py` — a Python port of Guardian Gold v5.5's live signal logic — as a **tracked, public** file, together with tests that restate the locked filter semantics and a README that publishes the parameter set and certifies the port reproduces the native strategy to **0.46% net / 1.76% PF over the full 52-trade window**. The strategies remain live (venue pivot to CME-micro futures-prop, not a strategy retirement), so the edge the posture protects is still running.

**What the parity directory disclosed (task item 1):** the complete signal skeleton — full
entry/exit parameter set, session/hour-block/day filters, execution-model facts (fill timing,
grace stop, slippage, dd_protection posture), the chart-TZ-not-UTC landmine, and Pine source
line numbers. *(2026-08-14: the literal parameter values originally listed here are redacted
from the public tree per [`2026-08-14-repo-public-visibility-transition.md`](2026-08-14-repo-public-visibility-transition.md)
— this ADR is itself evidence of what was disclosed, so restating the values here would
re-disclose them.)*

**The two findings that frame the decision:**

1. **The letter of the posture was not violated; its intent was.** The gitignore protects `.pine` bytes. But the parent ADR's own §3/§5 invoke an "edge-protection doctrine" (no private Pine to third-party compilers; live account walled off) — and a tracked, parity-*validated*, executable reproduction of the locked strategy is a stronger disclosure than the Pine upload that doctrine forbids. Public tracking of the port was simply never weighed in the 2026-06-23 decision.
2. **The port is not a novel disclosure — the skeleton was already public.** `LOCK.md` (tracked) publishes the full locked-config block; `oanda_stage1/guardian_stage1.py` is a prior committed Python implementation of the same predicates; `codification/primitives.py` quotes `recoveryLong` verbatim; the filter-sweep README enumerates every filter; the 2026-06-28 MQL5 spec publishes the parameter row. What the parity port *added* is the packaging: one runnable module + a validation certificate + a runbook. That is an amplification-of-access difference, not an information-content difference.

**Decision driver (one sentence):** an executable, validated clone of a locked live strategy should not ship in every fresh public clone when the stated posture holds the same logic's source privately — and the remediation record must not pretend removal un-discloses anything, because git history (public since 2026-06-23) already serves the bytes.

---

## §2 — Decision

1. **Untrack** `guardian_signal.py` + `test_guardian_signal.py` (gitignore entries; working copies kept locally), extending the `**/*.pine` edge-protection class to executable Python ports of locked strategy logic. **Effective this commit.**
2. **Hash-pin** both files in `lab/analysis/legacy/guardian_parity_2026-06-23/PORT_MANIFEST.sha256` (tom_spx `PINE_MANIFEST.sha256` convention: LF-normalized SHA256, restore + verify commands inline). The manifest is the durable integrity record; the restore runbook is mandatory because pulling the untracking commit deletes the operator's tracked working copies — the exact 2026-06-16 tom_spx loss mode.
3. **Accept history exposure explicitly — no purge.** The bytes remain publicly retrievable (`git show dc07898:<path>`); this decision **limits amplification (fresh clones, browsable HEAD), not disclosure**. A history rewrite was considered and rejected (§3).
4. **Standing rule:** new Python/MQL5/other-language ports of locked strategy logic land **gitignored + hash-pinned by default**, never tracked. Candidate-scaffold ports (no live edge, e.g. R&D-pipeline candidates) are out of scope — they already regenerate from concept YAML.
5. **Keep tracked:** `next_open_engine.py` (generic TV execution-model infra — next-open/grace/slippage mechanics are TV semantics, not Guardian's edge; the MQL5 spec references it as reusable), `run_parity.py` (driver; port now lazily imported so `test_run_parity.py` stays green on public clones/CI), and the README including its parameter one-liner — redacting one mirror while `LOCK.md`'s canonical block stays tracked would be theater.
6. **Forward-route (observation routing → Forward, operator decision):** does the *parameter-transcription* class stay public — `LOCK.md` locked-config blocks (all four strategies), the MQL5 conversion spec's strategy table, `codification/primitives.py` defaults, filter-sweep README, `oanda_stage1` frozen port? Cheapest falsification first: this is a value-of-secrecy judgment only the operator can make (the information is already public in history regardless; the question is whether HEAD keeps re-publishing it). Not decided here — it touches lock-governance artifacts.

**Scope:** public-clone posture / repository governance only. No strategy parameter, allocation, `dd_protection` constant, Pine source, or MC anchor is touched.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| **History purge** (`git filter-repo` + force-push) | Does not un-disclose: the repo has been public since 2026-06-23 (forks, clones, caches, archives are outside our control) — a purge buys amplification-reduction we already get from untracking, at the cost of breaking every clone/PR and rewriting shared history. No repo precedent: the pre-prune-2026-06-05 pattern deliberately *keeps* history retrievable. |
| **Archive-evict per the pre-prune pattern** (delete from working tree, retrieve via tag) | Wrong for *live tooling*: the parity harness is operationally useful for the active spot→futures re-mapping work. Gitignore-with-local-copy (the Pine pattern) preserves utility; eviction would force a history checkout on every use. |
| **Do nothing / accept-and-document only** | Leaves an executable, validated clone of a live locked strategy shipping in every fresh clone, directly against the parent ADR's own edge-protection doctrine. The marginal cost of untracking is one lazy-import shim. |
| **Full class-wide redaction now** (also strip `LOCK.md` config block, MQL5 spec table, codification defaults, filter-sweep README, oanda_stage1) | Touches lock-governance artifacts and a large doc surface for near-zero information effect (all of it is in public history); the value-of-secrecy tradeoff is an operator call → routed Forward (§2.6), not bundled into this commit. |
| **Untrack the whole parity directory** (engine + driver + README too) | Over-reach: `NextOpenEngine` encodes TV execution semantics, not Guardian's edge, and is referenced as reusable infra by the 2026-06-28 MQL5 spec; the README's verdict is the §4 falsifier record of the parent ADR. |

---

## §4 — Falsifier (revert trigger)

**H (falsifiable):** If the port class is untracked with hash pins + a restore runbook, then (a) the operator's local copies remain present and manifest-verified at each quarterly review (next: 2026-08-08, alongside the standing regime-trigger date), and (b) no new tracked file re-introduces executable locked-strategy port logic (audit hook grep below stays clean); **otherwise** this untracking scheme is **falsified** as operationally unworkable.

**Revert trigger:** if (a) fails — a local copy is lost or fails manifest verification and cannot be restored from the pinned SHA (the tom_spx loss mode recurring *despite* the manifest) — revert to tracked-with-narrow-exception (the `tom_spx/tom_test_spx500.pine` pattern: commit the source, keep the hash pin), because durability then outweighs amplification control for a file whose bytes are already public. If (b) fails twice (two separate tracked-port incidents), the standing rule is not self-enforcing — escalate to a mechanical gate (extend `scripts/check_pine_manifest.py`-class checking to port manifests) rather than more doctrine.

**Trigger check schedule:** quarterly reviews (2026-08-08, 2026-11-08, …) via the §10 hooks; event-driven on any new locked-strategy port landing.

---

## §5 — Forbidden moves (under this ADR)

- **Purging or force-rewriting public history to "clean up" the exposure** — it breaks clones/PRs and does not un-disclose; the pre-prune precedent keeps history. Tempting as the "thorough" fix; rejected in §3.
- **Presenting this untracking as having closed the disclosure** — in any doc, PR, or memory. The bytes are public at `dc07898` and in every fork. The honest claim is amplification-limiting only.
- **Redacting `LOCK.md`'s locked-config block (or the MQL5 spec table) unilaterally in this change** — tempting for coherence, but those are lock-governance artifacts and the class-wide question is the operator's (§2.6 Forward).
- **Porting the next locked strategy (Aegis/DJ30/NAS100) into a tracked path because "Guardian already leaked"** — prior leakage is not a license; §2.4 makes gitignored + hash-pinned the default.
- **Registering the untracked port as a `.gitignore` narrow *exception* later without re-running this ADR's calculus** — the tom_spx exception was justified by RESOLVED-ABSENT / no-live-edge; Guardian is the opposite case.

---

## §6 — Consequences

**Positive:**
- Fresh public clones no longer ship an executable, parity-validated reproduction of a live locked strategy; the posture text (CLAUDE.md) now states three gitignored classes and what each actually protects.
- The governance record is honest: history exposure is accepted in writing, with the retrieval SHA named, instead of silently implied away.
- The standing default (§2.4) closes the gap for the MQL5 conversion work now starting — those ports land private-by-default.

**Negative (real cost):**
- Public-clone reproducibility of the Guardian parity result is gone (was already gated on gitignored vendor CSVs, so the practical loss is small; `test_run_parity.py` + `test_next_open_engine.py` still run everywhere).
- The operator must restore two working copies after pulling this commit (runbook in `PORT_MANIFEST.sha256` and the directory README) — a real loss-risk window, mitigated by the pinned public SHA.
- The two files no longer receive CI test coverage on GitHub runners (locally 9/9 still must pass — §10).

**Risks:**
- Manifest drift if the operator legitimately edits the port later (M-9 class) → re-pin in the same change; the §4(b) escalation path adds a mechanical gate if doctrine alone fails.
- The Forward question (§2.6) going stale → it is attached to the quarterly review dates, not left free-floating.

---

## §7 — Implementation plan

- **Phase 0** — §0 reads (done 2026-07-01, this ADR).
- **Phase 1** (this commit) — gitignore entries; `git rm --cached` both files; `PORT_MANIFEST.sha256`; lazy import in `run_parity.py`; README §Local-only files + file-table annotations; CLAUDE.md third posture bullet; parent-ADR change-history row; this ADR.
- **Phase 2** (operator, on pull) — restore the two working copies per the runbook; verify against the manifest; re-run `test_guardian_signal.py` (expect 9/9).
- **Phase 3** (operator, unscheduled) — decide the §2.6 Forward question on the parameter-transcription class; record as an ADR amendment or a separate ADR.

---

## §10 — Audit hooks (runnable)

```bash
# 1. The two port files are NOT tracked (expect: no output)
git ls-files | grep -E 'guardian_parity_2026-06-23/(test_)?guardian_signal\.py'

# 2. Gitignore entries present (expect: 2 matching lines)
grep -c 'guardian_parity_2026-06-23/.*guardian_signal\.py' .gitignore

# 3. Local copies present + manifest-verified (operator machines; expect: two matching digests)
python -c "import hashlib,pathlib;d=pathlib.Path('lab/analysis/legacy/guardian_parity_2026-06-23');[print(hashlib.sha256((d/n).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),'',n) for n in ('guardian_signal.py','test_guardian_signal.py')]"
grep -E '^[0-9a-f]{64}' lab/analysis/legacy/guardian_parity_2026-06-23/PORT_MANIFEST.sha256

# 4. No NEW tracked executable ports of locked strategy logic (expect: NO output;
#    excluded = frozen-historical oanda_stage1 + codification primitives already
#    accepted in §1, and run_parity.py which only NAMES the symbol in its lazy import)
git grep -l "GUARDIAN_V55_CONFIG\|emaSlowLen" -- '*.py' | grep -v 'oanda_stage1\|codification\|guardian_parity_2026-06-23/run_parity'

# 5. Public-clone test surface still green without the port (CI equivalent):
#    test_run_parity.py imports run_parity without guardian_signal present
python lab/analysis/legacy/guardian_parity_2026-06-23/test_run_parity.py     # expect 3/3
python lab/analysis/legacy/guardian_parity_2026-06-23/test_next_open_engine.py  # expect 9/9

# 6. Locally (port restored): signal tests still pass
python lab/analysis/legacy/guardian_parity_2026-06-23/test_guardian_signal.py   # expect 9/9
```

---

## Verification

```bash
python scripts/check_brief.py docs/adr/2026-07-01-guardian-pyport-public-tracking.md --type adr
# Expected: PASS

# Rule-0 anchors: the disclosure object's public retrieval SHA is real
git cat-file -e dc07898:lab/analysis/legacy/guardian_parity_2026-06-23/guardian_signal.py && echo OK

# Cross-reference: LOCK.md's locked-config block is redacted as of 2026-08-14 (expect no match)
grep -n "## Locked config (transcribed" core/strategies/_archive/guardian/LOCK.md
```

---

## Addendum — 2026-07-01 (same day) — visibility premise corrected

The programme audit this date surfaced that this ADR's §0 anchor "Repo is public" and
its §3/§6 reasoning ("public since 2026-06-23", history-purge rejected because exposure
already occurred) rest on an **unverified platform-state claim** — the exact
doc/reality skew class (verify-source / M-12) the audit flags, appearing inside a §0
verification block.

**Verified fact (does not edit the decision above):** `gh repo view` returns
`isPrivate: true` / `visibility: PRIVATE` as of 2026-07-01 (operator also confirmed via
the GitHub Settings screen). The `PublicEvent` API returned nothing. `Q-VISIBILITY-1`
(`b7eb3e5`, 2026-06-06) had flipped the repo **private**; `guardian_signal.py` first
landed **2026-06-23** (`d9e8dd8`) — *after* privatization.

**Consequence:** the "history exposure already happened" premise is uncertain and the
conservative reading is that the port bytes **may never have been publicly served**
(actual exposure ≤ the exposure this ADR assumed and accepted). This makes the accepted
cost *smaller*, not larger — **the untracking + hash-pin decision (§2) stands unchanged**;
no re-open. What changes:

1. The §2.6 parameter-transcription Forward question is **re-scoped as contingent on the
   re-publicization decision** — if the repo stays private, the transcription-exposure
   surface is moot until it goes public again.
2. Do **not** cite "public since 2026-06-23" as fact anywhere downstream without the
   audit-log timeline. Operator to confirm the full public↔private history
   (GitHub Settings → Audit log) at convenience; a further addendum records it if it
   changes the picture.

Never edit §3/§4/§6 in place — this addendum supersedes their visibility premise only.

---

## Addendum — 2026-08-14 — partially superseded by the public-visibility transition ADR

The §2.6 Forward question ("does the parameter-transcription class stay public") is now
**resolved**, and the "repo is currently private" premise this ADR's Addendum re-scoped
around is now **superseded**, by
[`2026-08-14-repo-public-visibility-transition.md`](2026-08-14-repo-public-visibility-transition.md)
(`Supersedes: 2026-07-01-guardian-pyport-public-tracking.md in part`). That ADR: (a) the
operator has decided to go public via a fresh-repo transplant, not an in-place flip; (b)
resolves §2.6 toward **redaction** — the 6 tracked `LOCK.md`-family files' parameter and
backtest-results blocks are stripped to name/version/lock-date/risk%/hash before the new
public repo is seeded.

**This ADR's §2 untracking decision is unaffected and stands unchanged** — ports still land
gitignored + hash-pinned by default; `lab/archive/oanda_stage1/guardian_stage1.py` (named in
this ADR's §0 as a prior tracked disclosure) is picked up as a residual gap by the 2026-08-14
ADR's own remediation (it was never gitignored despite the standing rule here) and gets
untracked there.

Never edit §2/§3/§4/§6 in place — this addendum records the partial supersession only.

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-01 | Initial authoring: disclosure assessment of the publicly-tracked Guardian port; untracking + hash-pin executed; history exposure accepted explicitly; parameter-transcription class routed Forward | Joshua + Claude Code |
| 2026-07-01 | Addendum: visibility premise corrected — repo gh-verified PRIVATE; port landed after 2026-06-06 privatization so exposure may never have occurred; decision unchanged, Forward question re-scoped contingent-on-re-publicization | Joshua + Claude Code (programme audit) |
| 2026-08-14 | Addendum: partially superseded by `2026-08-14-repo-public-visibility-transition.md` — §2.6 Forward question resolved toward redaction; "stays private" premise superseded; §2 untracking decision unchanged | Joshua + claude.ai |
| 2026-08-14 | Non-material: §1's "What the parity directory disclosed" paragraph had the literal parameter values it was quoting as evidence redacted (this ADR itself ships in the public tree; restating the values would re-disclose them). No change to the decision, findings, or reasoning — same redaction pass as the row above | claude.ai |
