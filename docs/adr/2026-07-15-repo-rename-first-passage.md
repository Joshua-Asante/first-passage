# ADR 2026-07-15 — Rename the operation identity `multi_firm_operations` / `multi-firm-operations` → First Passage

**Status:** `Accepted` — operator-ratified 2026-07-20 (chat). Execution via design [`docs/superpowers/specs/2026-07-20-first-passage-rename-and-prune-design.md`](../superpowers/specs/2026-07-20-first-passage-rename-and-prune-design.md); Stream 3 folder rename authorized by 2026-07-20 Addendum (gated on B6). No self-merge of identity/prune PRs.
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Decision date:** 2026-07-15
**Authors:** Joshua (decision — ratified 2026-07-20) + claude.ai advisor (drafting) + Claude Code (design) + Cursor (execution)
**Supersedes:** none. This is the first identity rename of the operation.
**Related:** `docs/adr/2026-06-05-monorepo-layer-boundaries.md` (the layer contract this rename must not disturb — `core/` untouched); `docs/adr/2026-07-11-gen1-pipeline-retirement.md` (format precedent for a low-reversibility structural change executed in isolation with a grep-gated audit); the retirement-ADR lineage (`2026-06-12-notion-surface-retirement`, `2026-06-17-dukascopy-retirement`, `2026-06-24-oanda-retirement`) whose provenance-not-rewrite discipline this copies.
**Layer:** infrastructure (repo identity, packaging, branding). **Not** strategy/risk-control: no Pine source, no `dd_protection`/`firm_rules`/`portfolio_mc` constant, no allocation, no MC anchor (99.83/0.17/4.37), no `core/`. **Not** history: no ADR, brief, `docs/ltm/**`, SESSIONS log, or archived Notion note is rewritten.

---

## §0 — Rule 0 reads (production-source verification)

**Honesty preamble (load-bearing — do not strip at ratification).** Files below were **content-read via the Windows filesystem on 2026-07-15**, during the advisor session that authored this draft, and the whole-repo occurrence scan was run the same session (`Select-String 'multi.firm.operations'` across tracked + working-tree text files, worktrees and `.venv*` pruned). Git-log anchors are `git log -1 --format='%h %ci' -- <path>`, HEAD `7c86db2` on branch `claude/update-repo-docs-9ea48d`. Anchors marked **UNTRACKED** returned empty from `git log` — the file exists in the working tree but is not version-controlled (local mirror / local settings); this is itself a load-bearing finding (see §2, §5).

Files content-read (2026-07-15), anchors:

- `pyproject.toml` — anchor `67e0ef7` (2026-07-11). Confirms the single load-bearing packaging fact: `name = "multi-firm-operations"`, **`packages = []`, `py-modules = []`**, code resolved via `pythonpath = ["core","lab","ops","governance","."]`. **There is no importable `multi_firm_operations` namespace** — zero `import` statements depend on the name. This is what makes the rename surgical rather than a refactor.
- `.claude/skills/code-defect-debugging/SKILL.md` — anchor `1772f26` (2026-07-08). Four references anchor the skill's own trigger identity to "`multi_firm_operations`" (description line, §Overview, "component boundaries", audit-hook). A live skill whose self-description names the old identity — forward-load-bearing (its routing anchor drifts if the stack is renamed and the skill is not). Also observed: it already names sibling `prop-firm-challenge` while the active roster still ships `fxify-challenge` — a pre-existing, *unrelated* rename drift (see §5: not in scope here).
- `.claude/skills/brief-authoring/references/cc_handoff.md` — anchor `349719c` (2026-07-14). Line 6: `**Repo:** \`multi_firm_operations\``. This is a **template field**: every future CC handoff authored from it stamps the old identity. This is the actual decision driver (see §1).
- `README.md` — anchor `7c86db2` (2026-07-15). Front-matter identity/branding uses "Multi-firm operations".
- `CLAUDE.md` — anchor `fad8984` (2026-07-14). Top identity line names the operation.
- `STATE.md` — anchor `7c86db2` (2026-07-15). Identity references (2 hits).
- `ops/cli.py` — anchor `8c461bc` (2026-07-11). L2 docstring + L152 argparse `description="Multi-firm operations CLI"` — user-facing help text only; no functional dependency on the name.
- `Makefile` — anchor `7c86db2` (2026-07-15). L1 comment header only.
- `docs/adr/2026-07-11-gen1-pipeline-retirement.md` — anchor `fad8984` (2026-07-14). Format precedent: low-reversibility structural change, executed in an isolated worktree, grep-gated, operator-ratified, history preserved via provenance rows rather than rewrite.

Files content-read, found **UNTRACKED** (git log empty) — edit-but-do-not-commit surface:

- `.claude/settings.local.json` — **UNTRACKED**. L6–L7 hold the CC bash allowlist entries `git -C C:/Users/joshu/multi_firm_operations …` (absolute path). Local override file; not in the repo. Only needs editing **if the local folder is renamed** (it is not — see §2).
- `.agents/skills/code-defect-debugging/SKILL.md` — **UNTRACKED**. Local mirror of the `.claude/skills/` copy. Edit the mirror the same way, but do not `git add` it.
- `AGENTS.md` — **UNTRACKED**, and currently **not byte-identical** to `CLAUDE.md` (hash differs). Local mirror of `CLAUDE.md`; regenerate via the normal sync, do not track.

**Not read this session (not load-bearing for identity):** the historical corpus — 19 ADRs, `docs/briefs/**`, `docs/ltm/**`, `SESSIONS*.md`, archived Notion notes, `lab/archive/**`, `lab/analysis/<dated>/**` and their `.json`/`.txt` outputs. These carry the old name because it *was* the name when they shipped. They are records, not live text (see §2 / §5).

---

## §1 — Context

The operation is referred to, thought about, and positioned (including as the AI-agent-reliability career wedge) as **First Passage**. The repo it lives in is still named `multi_firm_operations` — a descriptive-legacy label from the multi-firm prop-ops era, now diverged from the brand. This is mostly cosmetic drift, with one exception that makes it a real decision rather than a someday-nicety: the `cc_handoff.md` template's `**Repo:**` field (§0) **mints `multi_firm_operations` into every future CC handoff brief**. Left alone, the legacy identity keeps propagating forward into new load-bearing artifacts indefinitely.

The scan surface looks alarming — **494 files / 999 matches** of `multi.firm.operations` — but the production read (§0) decomposes it into almost entirely inert mass:

- **~half the matches are in `.claude/worktrees/*`** — three transient branch checkouts (`open-items-inqhiori`, `operator-phase0`, `q-harv-1-successor-preq` [locked]) that duplicate the whole tree. They inherit from `main` on rebase/merge or vanish on prune. Editing them by hand is wrong.
- **The large majority of the remainder is immutable history** — the 19 ADRs, briefs, `docs/ltm/**` (long-term-memory archive), the SESSIONS logs (`SESSIONS-2026-Q2.md` alone is 66 hits), the archived Notion notes, and retired `lab/` one-offs. Under the repo's annotate-never-delete / history-is-a-record discipline (the retirement-ADR lineage), these are not rewritten. The old name in a 2026-05 session log is a *true statement about 2026-05*.
- **There is no import namespace** (`packages=[]`, `py-modules=[]`; §0). Zero `import` statements change.

So the actual load-bearing surface is **~6 tracked files + 3 untracked mirrors**, not 494.

**Decision driver (one sentence):** the brand is First Passage, the repo identity is not, and the `cc_handoff.md` template actively propagates the legacy identity into every new artifact — so rename the identity surgically (packaging + GitHub slug + brand + the live forward-propagating anchors), while explicitly preserving history and deferring the higher-risk local-folder rename.

---

## §2 — Decision

**Decision (proposed):** Rename the operation's canonical identity from the legacy `multi_firm_operations` / `multi-firm-operations` to **First Passage**, across three independent name-forms, touching only the live identity surface and never the historical record or `core/`. Execution runs via the companion CC handoff (`docs/briefs/handoffs/2026-07-15-cc-handoff-repo-rename-first-passage.md`), on a branch, operator-ratified, no self-merge. The rename is `git`-reversible by construction.

Three name-forms (recommended canonical values; the kebab-vs-underscore slug choice is an operator confirm — see §0.5 of the handoff):

| Form | From | To |
|---|---|---|
| GitHub repo slug | `multi_firm_operations` | `first-passage` (kebab; operator may prefer `first_passage` to match the old underscore) |
| Python distribution name (`pyproject.toml`) | `multi-firm-operations` | `first-passage` (kebab is already the existing convention for the dist name) |
| Display / brand | "Multi-firm operations" | "First Passage" |

Per-surface disposition:

| Surface | Disposition | Note |
|---|---|---|
| `pyproject.toml` `name` (+ any brand phrase in `description`) | **CHANGE** | The one packaging edit. Then delete stale `multi_firm_operations.egg-info/` and re-run `pip install -e .` → regenerates `first_passage.egg-info`. |
| `.claude/skills/code-defect-debugging/SKILL.md` (4 refs) | **CHANGE** | Live skill trigger identity. Mirror the edit into the UNTRACKED `.agents/skills/…` copy (do not `git add` the mirror). |
| `.claude/skills/brief-authoring/references/cc_handoff.md` L6 `**Repo:**` | **CHANGE** | The forward-propagating template field — the decision driver. |
| `README.md`, `CLAUDE.md`/`AGENTS.md`/`STATE.md` identity lines, `ops/cli.py` (L2, L152), `Makefile` L1 | **CHANGE (branding)** | Cosmetic, no functional dependency. `AGENTS.md` is an UNTRACKED mirror — regenerate, don't track. |
| GitHub repo slug | **CHANGE (operator-only)** | GitHub Settings → rename. Auto-redirects old URLs. Then `git remote set-url origin` on each clone (redirect covers it regardless). Not a CC action — it is an account/settings change. |
| Local working-tree folder `C:\Users\joshu\multi_firm_operations` | **DO NOT RENAME in this ADR** | Decoupled from the identity rename. Deferred to an optional, separate, deliberate step because of the git-worktree hazard (§4/§5): four linked worktrees — three under `.claude/worktrees/`, one **external** at `C:\Users\joshu\wt-kbudget-rescreen`, plus `.worktrees/sfrisk-f4-days-to-first-skim` — store the absolute main-repo path in their `.git` pointers; renaming the folder breaks every linkage until `git worktree repair`. |
| `.claude/settings.local.json` allowlist (2 abs-path lines) | **NO CHANGE** | Only stale if the folder is renamed, which it is not. Revisit with the deferred folder rename. |

**Explicitly NOT changed (history + evidence — annotate-never-delete):** any ADR, `docs/briefs/**`, `docs/ltm/**`, `SESSIONS*.md`, archived Notion note, `lab/archive/**`, `lab/analysis/<dated>/**`, or any `.json`/`.txt` run-output. The old identity in these is a true record of the past. The `.claude/worktrees/*` duplicates are also not hand-edited.

**Effective:** on the ratification commit, only after the companion handoff's Phase 0 grep-gate confirms the live surface still matches this enumeration. **Scope:** the ~6 tracked files + 3 untracked mirrors above, plus the GitHub slug and `pip install -e .` regen. No `core/`, no Pine, no locked constant, no history file.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| **Blanket `sed`/find-replace `multi_firm_operations → first_passage` across the tree** | Rewrites 19 ADRs, the Q2 session log (66 hits), the whole `docs/ltm/**` archive, and 4 worktrees. Falsifies immutable records (the old name in a 2026-05 log is a true statement about 2026-05) and re-writes transient worktree checkouts that should inherit from `main`. This is exactly the history-mutation the retirement-ADR lineage exists to forbid. |
| **Rename the local folder in the same pass** | Breaks all four git-worktree `.git` pointers (incl. the external `wt-kbudget-rescreen`) and staleness the `.claude/settings.local.json` allowlist. Requires `git worktree repair` and an allowlist edit. Higher risk, and fully separable from the identity rename — so decouple and defer, don't bundle. |
| **Do nothing / keep `multi_firm_operations`** | Tolerable for the historical corpus, but the `cc_handoff.md` `**Repo:**` field keeps minting the legacy identity into every *new* handoff, and the code-defect-debugging skill's trigger anchor stays wrong. The forward-propagation is the cost that doing nothing does not stop. |
| **Rename the dist name but not the GitHub slug (or vice-versa)** | Leaves brand/identity split across surfaces (repo says one thing, `pip show` says another). The three forms are independent operations but should land together for identity coherence; splitting them is a half-rename that invites confusion. |
| **Also reconcile the `fxify-challenge → prop-firm-challenge` skill drift while here** | A *different* rename (skill roster), unrelated to the repo identity. Bundling it is scope creep and would make the diff hard to spec-audit. Flag it (§0 noted it) and handle it in its own pass. |

---

## §4 — Falsifier (revert trigger)

A rename's falsifier is: *did the change break a live path or lose a resolvable reference the replacement does not cover?* Because git preserves every byte and the GitHub rename auto-redirects, the revert is cheap — so the bar to fire is deliberately low.

**H (revert trigger, binary):** If `pip show first-passage` fails, OR `python ops/cli.py --help` errors on import, OR any live (non-archived) reference to the old identity still resolves in the code path within one week of execution, then this ADR is **FALSIFIED** and reverted (`git revert` + re-scope the grep); otherwise the rename is **RESOLVED**. (The historical-record match count staying unchanged is a *confirming* condition, not a falsifying one — see §10 hook 3.)

- **Live-reference falsifier:** if within **one week of execution** any live surface fails to resolve because of a missed edit — `pip show first-passage` fails, `ops/cli.py --help` errors on import, the editable install can't be re-created, CI breaks, or a live (non-archived) script raises on the changed name — then the surgical set was under-scoped. **Revert action:** `git revert` the rename commit, restore, re-run the Phase 0 grep to find the missed reference, re-execute. Checkable: `pip show first-passage` succeeds; `python ops/cli.py --help` exits 0; `git worktree list` errors-free.
- **Worktree-integrity falsifier (only if the deferred folder rename is later done):** if after a folder rename `git worktree list` reports broken linkages that `git worktree repair` does not fix → the folder-rename step was mis-sequenced; restore the folder name, repair, and re-plan the folder move as its own ADR.
- **Premise falsifier (would withdraw this ADR before execution):** if "First Passage" is not the intended name, or the operator prefers to keep `multi_firm_operations`, or picks a different brand — withdraw; nothing has executed.

**Trigger check schedule:** the one-week live-reference check fires on the execution date + 7 days; thereafter rides the standing quarterly review (next: 2026-08-08). A rename that has resolved cleanly for one week and one quarter is settled.

---

## §5 — Forbidden moves (under this ADR)

- **Any blanket find-replace across history or worktrees.** Identity/machinery only. ADRs, briefs, `docs/ltm/**`, SESSIONS logs, archived notes, and `.claude/worktrees/*` are never touched. Rewriting a historical record to carry the new name is `p`-hacking the past.
- **Renaming the local folder in this change.** Deferred by decision (§2). Doing it here without `git worktree repair` breaks four worktrees, including the external `wt-kbudget-rescreen`.
- **`git add`-ing the untracked mirrors.** `.claude/settings.local.json`, `.agents/**`, and `AGENTS.md` are local-only. Edit where needed, regenerate per the normal sync, but do not pull them into version control as a side effect of this rename.
- **Bundling the `fxify-challenge → prop-firm-challenge` skill rename.** A separate, unrelated rename. Ruled out of scope in §3; surfacing it is fine, fixing it here is scope creep.
- **Touching `core/`, any Pine source, any locked constant (`dd_protection`/`firm_rules`/`portfolio_mc`), the MC anchor, or any allocation.** A diff that touches these is an integrity failure of this change — it is an identity rename, nothing else.
- **Self-merging.** claude.ai drafts and CC executes on a branch; the operator ratifies and merges. No commit to `main` without the go.
- **Loosening §4 mid-execution.** If the live-reference check looks like it will fire, do not quietly redefine "resolves cleanly." Revert, find the miss, re-run.

---

## §6 — Consequences

**Positive:**
- **Identity coherence** — GitHub slug, `pip show`, and brand all read First Passage; the operation's name matches how it is referred to and positioned.
- **Forward-propagation fixed** — the `cc_handoff.md` `**Repo:**` field and the code-defect-debugging trigger anchor now stamp/route the correct identity into every future artifact. This is the load-bearing win.
- **Zero blast radius on code** — no import surface, no `core/`, no locked constant; the change cannot affect strategy behavior, risk controls, or the MC anchor.
- **History stays honest** — the record of the `multi_firm_operations` era is preserved verbatim, exactly as with the dukascopy/oanda/notion retirements.

**Negative (real costs):**
- **GitHub redirect caveat** — old URLs redirect after the slug rename, but the old slug must not be re-used by another repo or the redirect breaks; a one-time `git remote set-url` on each clone is cleanest.
- **One-time editable-install regen** — delete `multi_firm_operations.egg-info/`, `pip install -e .`.
- **Two-machine sync** — if a second clone exists beyond this one working copy (everything under `C:\Users\joshu` suggests CC and Cursor share one checkout), repeat the remote update there.

**Risks:**
- **A missed live reference** breaks a path. Mitigation: the Phase 0 grep-gate enumerates the surface before edits, and §4's one-week live-reference falsifier catches anything that slips.
- **Later folder rename breaks worktrees.** Mitigation: explicitly deferred; when done, `git worktree repair` + allowlist edit as its own step.

**Downstream artifacts that need updating:** `pyproject.toml`; `code-defect-debugging/SKILL.md` (×2 mirrors); `cc_handoff.md` template; `README.md`; `CLAUDE.md`/`AGENTS.md`/`STATE.md` identity lines; `ops/cli.py`; `Makefile`; `first_passage.egg-info` (regenerated); GitHub slug; `git remote` URL. **Not** updated: any history/evidence file (by design).

---

## §7 — Implementation plan

Mechanical execution is delegated to the companion CC handoff: **`docs/briefs/handoffs/2026-07-15-cc-handoff-repo-rename-first-passage.md`**. This ADR is the decision; the handoff is the vehicle.

- **Phase 0 (in handoff)** — read the §0 files, confirm anchors still current, and **re-run the occurrence grep to confirm the live surface still matches §2's enumeration** (drift check). Surface the kebab-vs-underscore slug choice (§0.5). BLOCKING before any edit.
- **Phase 1 (in handoff, CC)** — edit the ~6 tracked files + 3 untracked mirrors per §2, on a dedicated branch (`rename/first-passage`). No history, no worktrees, no `core/`.
- **Phase 2 (in handoff, CC)** — delete stale egg-info, `pip install -e .`, smoke test (`pip show first-passage`, `python ops/cli.py --help`), run the grep-gate proving the live surface is clean **and** the historical match-count is unchanged.
- **Phase 3 (operator-only, not CC)** — GitHub Settings slug rename; `git remote set-url origin`; PR the branch; operator ratifies and merges; flip this ADR to `Accepted`. The deferred local-folder rename (+ `git worktree repair` + allowlist edit) is a **separate future step**, not part of this ADR.

---

## §10 — Audit hooks (runnable)

```bash
cd "C:/Users/joshu/multi_firm_operations"   # path unchanged (folder rename deferred)

# 1. Live identity surface is clean (post-execution → expect EMPTY)
git grep -nE 'multi.firm.operations' -- pyproject.toml ops/cli.py Makefile README.md CLAUDE.md STATE.md \
  .claude/skills/code-defect-debugging/SKILL.md .claude/skills/brief-authoring/references/cc_handoff.md

# 2. New identity is in place
grep -n 'name = "first-passage"' pyproject.toml
pip show first-passage >/dev/null && echo "dist OK"
python ops/cli.py --help >/dev/null && echo "cli imports OK"
ls -d first_passage.egg-info 2>/dev/null && echo "egg-info regenerated"
! ls -d multi_firm_operations.egg-info 2>/dev/null && echo "stale egg-info gone"

# 3. History was NOT rewritten (the inversion assertion — expect these to STILL match)
#    We deliberately preserved the record. A DROP in this count means history was touched.
git grep -cE 'multi.firm.operations' -- 'docs/adr/**' 'docs/ltm/**' 'docs/briefs/**' | awk -F: '{s+=$2} END{print "history matches still present:", s}'
# Expected: unchanged from pre-execution baseline (record the baseline in the handoff closure)

# 4. core / Pine / locked constants untouched (expect EMPTY)
git diff --stat <ratification>~1..<ratification> -- core/ '*.pine' core/config/params.toml core/dd_protection.py

# 5. Worktrees intact (folder not renamed → expect no errors)
git worktree list

# 6. Untracked mirrors were NOT accidentally tracked (expect EMPTY)
git ls-files .claude/settings.local.json .agents AGENTS.md

# 7. GitHub slug + remote (operator step)
git remote -v   # expect origin → .../first-passage.git after Phase 3
```

---

## Verification

```bash
# Discipline check (mechanical)
python scripts/check_brief.py docs/adr/2026-07-15-repo-rename-first-passage.md --type adr
# Expected: all 6 checks PASS (§0 anchors populated 2026-07-15)

# Rule 0: anchors resolve
for f in pyproject.toml .claude/skills/code-defect-debugging/SKILL.md \
         .claude/skills/brief-authoring/references/cc_handoff.md ops/cli.py \
         docs/adr/2026-07-11-gen1-pipeline-retirement.md ; do
  git log -1 --format='%h %ci  '"$f" -- "$f"
done
# Expected: 67e0ef7 / 1772f26 / 349719c / 8c461bc / fad8984 respectively

# Untracked-mirror finding holds (expect EMPTY = untracked)
git log -1 -- .claude/settings.local.json .agents/skills/code-defect-debugging/SKILL.md AGENTS.md
```

Operator ratified 2026-07-20. Live grep-gate + smoke tests remain Stream-1 execution gates (see design §2.1 / ADR §4); Status `Accepted` records the decision, not completion of every downstream surface.

---

## Addendum — 2026-07-20 operator ratification + Stream 3 authorization

**Ratification:** Joshua approved the decision (kebab slug/dist `first-passage`, display brand "First Passage") and the corrected execution design. §0 audit corrections that supersede stale ADR/handoff prose for *execution* (not for historical §0 honesty):

1. Live edit surface is **8 tracked files** + derived `requirements-ops.lock` (not "~6").
2. Untracked mirrors `AGENTS.md` / `.agents/skills/…` are gone (commit `01a4045`); do not recreate.
3. Clean-surface grep must be **case-insensitive**: `git grep -inE 'multi[ _-]firm[ _-]operations'`.
4. HISTORY baseline is **dynamic** (capture pre-edit; 2026-07-20 snapshot was 200).
5. Lockfile regen uses **Python 3.12** pip-compile per `requirements-ops.lock` header.

**Stream 3 — local folder rename now authorized (gated):** The original §2 disposition "DO NOT RENAME the local folder in this ADR" is **superseded in part** by this Addendum. The folder move `C:\Users\joshu\multi_firm_operations` → `C:\Users\joshu\first-passage` is operator-authorized as a **separate Stream 3** under the design, fireable only after: Stream 1 merged; PR #451 merged; B6 dry-fire signed off; A2 husk deleted; full Windows quiescence (Cursor + CC closed). Canonical runbook: [`docs/notes/2026-07-20-first-passage-folder-rename-runbook.md`](../notes/2026-07-20-first-passage-folder-rename-runbook.md). Zero linked worktrees today → no `git worktree repair`. CC dual-state + Cursor reopen continuity are in-scope for Stream 3; identity file edits are not.

**Conservative prune:** Operator also authorized Stream 2 (C1 archive now with citation repairs; classify untracked outputs; C2 defer past B6). Prune does not alter this ADR's identity decision surface.

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-15 | Initial draft — `Proposed`; §0 anchors populated (HEAD `7c86db2`); companion CC handoff authored; awaiting operator ratification + slug-form confirm | claude.ai advisor |
| 2026-07-20 | Operator ratification → Status `Accepted`; §0 audit corrections + Stream 3 folder-rename authorization (B6-gated); companion design approved | Joshua (operator) + Cursor |
