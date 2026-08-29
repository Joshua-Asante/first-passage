# ADR 2026-06-04 — Methodology skills under version control, gated like production
**Status:** Accepted - ratified 2026-06-04; Rule-0 anchors confirmed on-disk during authoring (see blockquote header below for the full provenance note).
**Decision date:** 2026-06-04
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none

> **Status:** ACCEPTED 2026-06-04 — §0 anchors confirmed on-disk during authoring at HEAD `17ab0ad`; CC re-confirms in the companion handoff's Phase 0, then PO accepts.
> **Author:** Claude (Tech Advisor) — drafted for PO (Joshua) review.
> **Supersedes / relates to:** `2026-06-04-lean-portfolio-meta-layer.md` (provenance/audit discipline it installs); the 2026-06-04 advisor-session finding that the deployed skill set (11) and the repo's tracked skill set (2) diverge silently.
> **Provenance note:** built from the `brief-authoring` SKILL.md body structure (§0/§1/§2/§4/§5/§6/§10). The canonical `references/adr.md` template is not in-repo at `17ab0ad` — see §1; that absence is part of what this ADR fixes.

---

## §0 — Rule 0: production reads (confirm on-disk before ACCEPT)

| Claim this ADR relies on | On-disk confirmation | Provenance |
|---|---|---|
| Only two skills are version-controlled | `git ls-files \| grep -i skill` returns `.claude/skills/trade-capture/**` and `.claude/skills/trade-csv-reconcile/references/baselines.md` only | `17ab0ad` — **MATCH** |
| Methodology skills exist only as audit *subjects*, not tracked source | `docs/audits/2026-05-16-inqhiori-programme-audit.md`, `docs/lessons/2026-05-27-brief-authoring-traps-13-14-15.md` reference skills that are not themselves tracked | `17ab0ad` — **MATCH** |
| The drift-check mechanism already exists for a doc | `scripts/validate_params.py::check_claude_md` (~L300) hard-fails the pre-commit gate when CLAUDE.md's strategy table drifts from production constants | `17ab0ad` — **MATCH** |
| Skill checks exist but are NOT gated | `scripts/check_skill_enum_mirror.py`, `scripts/check_skill_notion_schema.py` exist with tests; `grep -r check_skill scripts/githooks/ .github/` returns nothing | `17ab0ad` — **MATCH** |
| The pre-commit gate is the load-bearing enforcement point | `scripts/githooks/pre-commit` runs `validate_params.py` always + conditional data-manifest check | `17ab0ad` — **MATCH** |
| `check_brief.py` (the brief validator every verification block invokes) is not in-repo | `ls scripts/check_brief.py` → absent | `17ab0ad` — **MATCH** |
| Deployed skills carry stale/duplicate content | `/mnt/skills/user/inqhiori-algorithm/SKILL.md` is declared superseded 2026-05-01 by `/mnt/skills/user/inqhiori/SKILL.md:15` yet remains live; `inqhiori/SKILL.md:§11` (L235–243) restates Striker v4.4 / S 1.00% / dd 1.0% / no NAS100, all stale vs `config/params.toml` (Striker v4.5 / 0.70% / 750%, NAS100 v1, dd C2 1.5%) | read on-disk 2026-06-04 at `/mnt/skills/user/` — **MATCH (and not git-tracked — the defect)** |

**§0-NOTES (PO actions before ACCEPT):**
1. Confirm the canonical home decision (§2.1) — `.claude/skills/` in this repo vs a dedicated skills repo.
2. CC re-runs the table above on-disk in the companion handoff's Phase 0 and reports any drift from `17ab0ad`.

---

## §1 — Context

Everything in this operation obeys one provenance rule — on-disk + commit hash > web > memory — enforced mechanically by `validate_params.py` in the pre-commit gate, which even keeps CLAUDE.md's operational table honest. The methodology layer is the single exception: nine skills (inqhiori, ooda-loop, programme-audit, brief-authoring, fxify-challenge, live-execution-journal, code-defect-debugging, pinescript-v6, notion-mcp-api-patterns) are deployed but live outside the repo, ungated, with no git history and no diff-against-locked. The cost is already realized and observable: a skill declared superseded on 2026-05-01 (`inqhiori-algorithm`) is still live, and `inqhiori` §11 carries an operational snapshot that has drifted stale on every line. Neither could have survived inside the repo — `validate_params.py` would have failed the commit. This ADR brings the rulebook under the same regime as the code it governs. The load-bearing part is not "tracked in git" — it is *gated*: tracking without enforcement is the ceremony this ADR's own falsifier (§4) is written to catch.

---

## §2 — Decision

**2.1 — Canonical home.** Methodology skills live in `multi_firm_operations/.claude/skills/`, alongside the two existing data-pipeline skills. The repo is the single source of truth. *[DEFAULT — flagged: a dedicated skills repo is the alternative; chosen against because this repo is already canonical, already has the CI/gate machinery, and `validate_params.py` must be able to reach skills to gate them. ASK to override.]*

**2.2 — Sync is one-directional: repo → deployed.** The deployed bundle at `/mnt/skills/user/` is a copy of the repo, never a source. Edits happen in-repo, pass the gate, then deploy. A drift check flags any deployed-vs-repo divergence. This permanently closes the 11-vs-2 split.

**2.3 — Prune on migration, not after.** The Algorithm's Delete step executes *during* the move:
- `inqhiori-algorithm` is **not migrated** — it is the superseded duplicate (per `inqhiori/SKILL.md:15`). It dies here.
- Every operational snapshot is stripped from methodology skills (`inqhiori` §11 first; then a grep sweep across all eight keepers for restated `version =` / `risk_pct` / dd / allocation constants). Those facts live in `config/params.toml` and the allocation ADRs; a skill may *point* to them, never restate them.

**2.4 — Gate the skills like production.** Add to the pre-commit gate, cheapest-first:
1. **Path-reference linter** (`scripts/check_skill_refs.py`): every repo path a skill cites must resolve. Highest-value, trivially mechanical; catches the most common rot.
2. **No-operational-constants guard:** fold a skills check into `validate_params.py` so a methodology skill restating a params.toml-class constant fails the commit — the direct fix for the §11 failure mode.
3. **Wire the existing dead checks** (`check_skill_enum_mirror.py`, `check_skill_notion_schema.py`) into the gate; optionally a superseded-duplicate guard.

**2.5 — Land the missing brief validator.** Bring `check_brief.py` into `scripts/` so every brief's verification block (and the two companion handoffs) actually resolves. brief-authoring coming under VC is the natural moment to fix this.

---

## §4 — Falsifiable hypothesis

**H:** If this is load-bearing rather than ceremonial, then after migration a deliberately-introduced defect in any methodology skill — a broken repo-path reference, or a restated operational constant — **fails the pre-commit gate** mechanically, and `inqhiori-algorithm` cannot reappear as a live skill undetected.

**Falsifier:** if a methodology skill can still drift stale (dead reference committed, operational constant restated) without the gate firing, then the skills were merely *tracked*, not *gated* — the move was ceremony, and the §2.4 gate is the part that was actually load-bearing. Repair: wire the gate or revert the tracking as cosmetic.

This is binary: the test is a commit of a broken skill that the hook must reject.

---

## §5 — Forbidden moves (genuinely tempting, ruled out)

1. **Tracking skills without wiring the gate.** "They're in version control now" feels like the win; it isn't. Ungated tracking is exactly what §4's falsifier condemns.
2. **Migrating skills with their stale snapshots intact** and "cleaning later." This carries the drift into git and the prune never happens. §2.3 makes the strip part of the move.
3. **Bidirectional sync.** Letting deployed-side edits flow back as truth recreates the split-brain. Repo → deployed only.
4. **Keeping `inqhiori-algorithm` "for reference."** It is a superseded ~95% duplicate with the same trigger surface; "reference" is how dead artifacts persist. Git history is the reference.
5. **Inventing a heavyweight skill schema** to match the data-pipeline skills' enum/Notion mirrors. Methodology skills have no enum to mirror; the right gate is a path-linter + constant-guard, not a schema.

---

## §6 — Gate / closure criteria

- **ACCEPTED** when §0 table is on-disk-confirmed by CC and §2.1 home is chosen by Joshua. Execution is the companion `2026-06-04-cc-handoff-methodology-skills-vc.md`.
- **RESOLVED (Progressive)** at next quarterly meta-layer `programme-audit`: §4's falsifier test passes (a broken skill commit is rejected), and `git ls-files | grep skill` shows the eight keepers tracked, zero `inqhiori-algorithm`, zero operational constants in methodology skills.
- **DEGENERATING** if skills are tracked but the gate was never wired (the §5 #1 trap) — prune the cosmetic tracking or wire the gate.
- Re-gate folded into the `programme-audit` quarterly meta cadence; no standalone cadence.

---

## §10 — Audit hooks (runnable)

```bash
# 1. Keepers tracked, duplicate gone
git ls-files .claude/skills/ | grep -c SKILL.md      # expect 10 (2 data + 8 methodology)
git ls-files | grep -c inqhiori-algorithm            # expect 0

# 2. No operational constants restated in any methodology skill
grep -rnE '(version[[:space:]]*=|risk_pct|0\.40|dd_protection.*1\.[05])' \
  .claude/skills/{inqhiori,ooda-loop,programme-audit,brief-authoring,fxify-challenge,live-execution-journal,code-defect-debugging,pinescript-v6}/ \
  && echo "VIOLATION — operational constant in methodology skill" || echo clean

# 3. Gate actually wired (the load-bearing check)
grep -qE 'check_skill_refs|check_skill_enum|validate_params' scripts/githooks/pre-commit \
  && echo "GATED" || echo "UNGATED — §4 falsifier would not fire"

# 4. Every repo path cited by a skill resolves
python scripts/check_skill_refs.py --all

# 5. Brief validator landed
ls scripts/check_brief.py && echo "validator present" || echo "MISSING — §2.5 open"
```

**Re-check cadence:** quarterly meta-layer `programme-audit`. If two cycles pass with hook #3 reading UNGATED, the tracking is decaying to ceremony — flag in the methodology audit.

---

## Decisions ratified 2026-06-04 (Joshua)

These ratifications close the §0-NOTES PO actions and pin the execution-time decisions:

1. **Canonical home = `.claude/skills/` in this repo (§2.1 default).** The dedicated-skills-repo alternative is declined; this repo is already canonical and already carries the gate machinery `validate_params.py` needs to reach the skills.

2. **No-constants guard is a CARVE-OUT, not blanket.** It guards the four *methodology* skills only — `{inqhiori, ooda-loop, programme-audit, brief-authoring}` — where restated operational constants are pure drift. The three *operational-reference* skills — `{fxify-challenge, live-execution-journal, code-defect-debugging}` — legitimately cite live ops state and are EXEMPT from the guard; they are migrated verbatim. (`pinescript-v6` carries no operational constants and is migrated verbatim outside the guard.) Stale constants found in the EXEMPT skills during migration are reported as follow-up recommendations, not silently edited.

3. **§0 table re-confirmed on-disk at HEAD `17ab0ad` by CC** during execution; the table held. The ADR file itself was the uncommitted artifact called out in §1 — it is now landed at `docs/adr/2026-06-04-methodology-skills-under-vc.md`.

## Addendum 2026-08-29 — three-skill migration premise falsified (DECAYED_UNDOCUMENTED, adr-decay-audit)

The full-corpus `adr-decay-audit` flagged §2.1's ratification note ("Decisions ratified 2026-06-04",
item 2) as `DECAYED_UNDOCUMENTED`: its premise that `fxify-challenge`, `live-execution-journal`,
and `notion-mcp-api-patterns` would be "migrated verbatim" into `.claude/skills/` as tracked,
gated, in-repo source no longer holds. This addendum is that discharge; the §0–§6, §10, and
"Decisions ratified" sections above stay byte-unedited as the historical record (Rule 14).

**What GSUB-1 found (2026-08-09).** GSUB-1 Phase 3 inventoried the deployed skill set and found:

- `fxify-challenge` and `live-execution-journal` are **platform-bundled `anthropic-skills:`
  plugins** — they have no file-level existence in this repo (or any repo) to "migrate verbatim";
  the migration premise assumed a tracked-source artifact that was never there. See
  `docs/pursuits/d7-fxify-challenge-plugin.md` and `docs/pursuits/d8-live-execution-journal-plugin.md`.
- `notion-mcp-api-patterns` was **archived, not migrated** — disposed of outright rather than
  landed under `.claude/skills/`. See `docs/pursuits/d6-notion-mcp-api-patterns-user-skill.md`.

**This does not falsify the ADR's core decision.** §2.1's canonical-home principle, §2.4's gating
machinery, and §2.5's brief-validator landing are unaffected and remain live and load-bearing —
`scripts/sync_skills.py` and `scripts/check_skill_refs.py` still cite this ADR's home/gate design
in production today. Only the narrow three-skill "migrated verbatim" disposition inside the
EXEMPT-carve-out ratification (item 2) is stale: it is superseded-in-effect by GSUB-1's actual
dispositions (two plugin-bundled, one archived), not by a reversal of the ADR's own reasoning.

**Disposition:** the three-skill migration plan named in this ADR's ratification note is
executed-as-superseded — overtaken by GSUB-1's per-skill findings rather than carried out as
originally planned. See `docs/briefs/GSUB-1-inventory-and-dispositions.md` for the full disposition
ledger.
