# ADR 2026-08-07 — W6: rail infra closures ($0 docs + tooling)

**Status:** `Accepted` — docs + dry-run-safe tooling; no arming
**Decision date:** 2026-08-07
**Authors:** Joshua (Posture-A direction) + Cursor (drafter)
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Related:** [SPEC S7](../spec/2026-08-07-loop-s7-repo-alignment-spec.md) · [alignment manifest](../notes/2026-08-07-posture-a-alignment-manifest.md) · [RUNBOOK](../notes/rail_build/RUNBOOK.md) · [GO ADR](2026-07-17-c1-rail-build-account-registration-go.md) · [operational Rule 15](../operational_rules.md)
**Layer:** rail ops docs + exporter stub. **$0 / K=0** — no deploy, no arm, no spend tally invention beyond documented facts.

---

## §0 — Rule 0 reads (verified 2026-08-07)

| Source | Anchor | What it pins |
|---|---|---|
| RUNBOOK B3 / Post-disarm | evidence export manual; Option-C checklist | Agent-memory-only relink + export steps |
| `ops/c1_rail/c1_rail_arm.py` | atomic config write for arm/disarm | Existing config writer for dry_run/armed_until |
| `requirements-research.txt` | pinned versions, not a hash lockfile | REPO_MAP “lockfile” claim overstates |
| grep desktop / always-on doctrine | empty | No owner surface for hosting doctrine |

---

## §1 — Context

Several rail infra facts lived only in agent memory or one-off session notes: CrossTrade→Tradovate relink under the 2-connection cap, post-disarm evidence export, volume-config edit discipline, and the desktop=console-only / always-on-hosting rule. Posture-A closes them as $0 docs + dry-run-safe stubs.

---

## §2 — Decision

1. **RUNBOOK** gains a CrossTrade→Tradovate **relink procedure** subsection (2-connection-cap fact; remedy when Option-C check is red).
2. **Committed exporter** `ops/c1_rail/export_session_evidence.py` — copies/exports events + evidence (+ optional alert acks) to a local directory; **dry-run safe** (default `--dry-run` prints plan; `--apply` copies). RUNBOOK Post-disarm lists the export step.
3. **Config writes:** document invocation of `c1_rail_arm.py` for arm/disarm and a committed **volume-config merge helper** `ops/c1_rail/write_volume_config.py` for non-secret key merges (aborts unless `dry_run` is true unless `--force-armed` — default refuse). Prefer these over hand-JSON edits (07-20/07-27 defect class). Notes in RUNBOOK + `deploy/c1_rail/README.md`.
4. **New operational Rule 15:** desktop = console-only for always-on processes; always-on hosting = Fly (or successor always-on host), not a personal desktop. Scope limited so it does not collide with cursor-fleet’s route-LOCAL rule for interactive sessions. Pointers in deploy README + c1-rail skill.
5. **`requirements-research.lock`:** **owed** — do not invent a fake lockfile. Recipe: recreate research venv per `requirements-research.txt` header, then `pip-compile` / `pip freeze` hash-pin into `requirements-research.lock` under a dedicated GO. REPO_MAP row corrected to name `.txt` as the live pin surface until the lock lands.
6. Pro-tier spend tally and NT8 dormant-fallback lines: refresh with dated notes only where facts are already in RUNBOOK (no new spend invented).

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Invent `requirements-research.lock` without a real freeze | Fake integrity surface |
| Require desktop always-on for the listener | Violates hosting doctrine; 07-31 brick class worse on laptops |
| Full NT8 teardown docs rewrite | Option-C dormant fallback still exists; dated note sufficient |

---

## §4 — Falsifier

**H:** An attended session can export evidence via the committed script without hand-scp recipes, and config key merges for M1 paths go through the writer while disarmed.

**FALSIFIED if:** exporter defaults to mutating the Fly volume; or Rule 15 is read as banning local Cursor/console interactive work.

---

## §5 — Forbidden moves

- Arming, deploying, or flipping `dry_run` under this ADR.
- Fabricating a lockfile hash set.
- Expanding Rule 15 to ban route-LOCAL interactive agent work.

---

## §6 — Gate

Same-PR docs + stubs. Lockfile generation = **owed**. Historical GO ADR Pro-tier addendum = optional follow-up (pointer ok).

---

## §7 — Audit hooks

```bash
python ops/c1_rail/export_session_evidence.py --help
python ops/c1_rail/write_volume_config.py --help
grep -n "Rule 15\|relink\|export_session_evidence\|write_volume_config" docs/notes/rail_build/RUNBOOK.md docs/operational_rules.md deploy/c1_rail/README.md
test ! -f requirements-research.lock && grep -n "owed\|requirements-research" REPO_MAP.md
```
