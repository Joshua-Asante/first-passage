# Persona Roster — Index

One row per persona defined under `docs/personas/`. See the
[design spec](../superpowers/specs/2026-08-18-loop-persona-hierarchy-design.md) for the full
architecture, panel mechanics, and independence rules this roster implements, and the
[ownership map](ownership-map.md) for which persona owns which part of the repo (directory skeleton
shipped; pursuit-level and per-artifact layers phased per
[the ownership-map plan](../superpowers/plans/2026-08-19-ownership-map-plan.md)).

**Verification:** `python scripts/check_personas.py`

**Front-Office-only spawnable roster, effective 2026-08-21** — see
[the narrowing ADR](../adr/2026-08-21-persona-hierarchy-front-office-only.md). Middle/Back-office
functions run as mechanical (code/script/doc) gates, not spawned personas; that ADR's §2 D2 maps
each retired seat to its mechanical equivalent.

| Persona | Tier | Office | Reports-to | Log |
|---|---|---|---|---|
| [CEO](ceo.md) | GRAND | N/A | — (top) | n/a — human, no persona log |
| [CIO](cio.md) | GRAND | Front | CEO | `cio-log.md` |
| [CFO](cfo.md) | GRAND | Cross-office | CEO | `cfo-log.md` |
| [Head of Research](head-of-research.md) | STRATEGIC | Front | CIO | `head-of-research-log.md` |
| [Head of Execution](head-of-execution.md) | STRATEGIC | Front | CIO | `head-of-execution-log.md` |
| [Falsifier Analyst](falsifier-analyst.md) | STAFF | Front | Head of Research | `falsifier-analyst-log.md` |
| [Pre-Registration Analyst](pre-registration-analyst.md) | STAFF | Front | Head of Research | `pre-registration-analyst-log.md` |
| [Research Analyst](research-analyst.md) | STAFF | Front | Head of Research | `research-analyst-log.md` |
| [TCA Analyst](tca-analyst.md) | STAFF | Front | Head of Execution | `tca-analyst-log.md` |

**Retired 2026-08-21** (Middle/Back-office C-suite/Senior-Manager seats + the two Back-office Staff
whose charters execute Head of Governance's own mandate — narrowed to Front Office per direct
operator instruction; each seat's function continues as the mechanical gate named in
[the narrowing ADR](../adr/2026-08-21-persona-hierarchy-front-office-only.md)'s §2 D2 table; full
charters preserved, not deleted, at [`docs/personas/archive/`](archive/); their log files stay in
this directory, frozen, per the design spec's own §6.7 step 3):
[CRO](archive/cro.md) → `cro-log.md`,
[Head of Risk & Sizing](archive/head-of-risk-sizing.md),
[Head of Validation](archive/head-of-validation.md),
[COO](archive/coo.md) → `coo-log.md`,
[Head of Engineering](archive/head-of-engineering.md),
[Head of Governance](archive/head-of-governance.md) → `head-of-governance-log.md`,
[Documentation Analyst](archive/documentation-analyst.md) → `documentation-analyst-log.md`,
[Research Registry Analyst](archive/research-registry-analyst.md) → `research-registry-analyst-log.md`.

**Archived 2026-08-19** (never spawned, zero log entries, kept for future reference rather than
deleted — tested against a real artifact outside all three domains, inconclusive rather than
negative, see [the audit](../notes/audits/2026-08-19-governance-friction-persona-panel-audit.md)):
Risk Analyst (Intraday), Model Validation Analyst, Robustness Analyst — full charters preserved at
[`docs/personas/archive/`](archive/). These were already Middle/Back-office Staff seats under the
now-retired Senior Managers above, so the 2026-08-21 narrowing does not change their disposition —
still archived, not restored. Re-propose any archived persona against a naturally-occurring,
better-fitting real artifact only alongside a superseding ADR — same intake-rule discipline GRAND
already applies to pursuits (§11), plus the 2026-08-21 ADR's own §5 forbidden-move on re-adding a
Middle/Back-office seat without one.

**Not on this roster:** Head of Engineering's staff were the literal Cursor worker agents dispatched
per packet under the existing `cursor-fleet` skill — ephemeral, not a persistent named persona; that
skill is now the mechanical equivalent for the whole seat, not just its staff (see
[`archive/head-of-engineering.md`](archive/head-of-engineering.md)).
