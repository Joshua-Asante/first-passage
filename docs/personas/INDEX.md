# Persona Roster — Index

One row per persona defined under `docs/personas/`. See the
[design spec](../superpowers/specs/2026-08-18-loop-persona-hierarchy-design.md) for the full
architecture, panel mechanics, and independence rules this roster implements, and the
[ownership map](ownership-map.md) for which persona owns which part of the repo (directory skeleton
shipped; pursuit-level and per-artifact layers phased per
[the ownership-map plan](../superpowers/plans/2026-08-19-ownership-map-plan.md)).

**Verification:** `python scripts/check_personas.py`

| Persona | Tier | Office | Reports-to | Log |
|---|---|---|---|---|
| [CEO](ceo.md) | GRAND | N/A | — (top) | n/a — human, no persona log |
| [CRO](cro.md) | GRAND | Middle | CEO | `cro-log.md` |
| [CIO](cio.md) | GRAND | Front | CEO | `cio-log.md` |
| [COO](coo.md) | GRAND | Back | CEO | `coo-log.md` |
| [CFO](cfo.md) | GRAND | Cross-office | CEO | `cfo-log.md` |
| [Head of Research](head-of-research.md) | STRATEGIC | Front | CIO | `head-of-research-log.md` |
| [Head of Execution](head-of-execution.md) | STRATEGIC | Front | CIO | `head-of-execution-log.md` |
| [Head of Risk & Sizing](head-of-risk-sizing.md) | STRATEGIC | Middle | CRO | `head-of-risk-sizing-log.md` |
| [Head of Validation](head-of-validation.md) | STRATEGIC | Middle | CRO | `head-of-validation-log.md` |
| [Head of Engineering](head-of-engineering.md) | STRATEGIC | Back | COO | `head-of-engineering-log.md` |
| [Head of Governance](head-of-governance.md) | STRATEGIC | Back | COO | `head-of-governance-log.md` |
| [Falsifier Analyst](falsifier-analyst.md) | STAFF | Front | Head of Research | `falsifier-analyst-log.md` |
| [Pre-Registration Analyst](pre-registration-analyst.md) | STAFF | Front | Head of Research | `pre-registration-analyst-log.md` |
| [TCA Analyst](tca-analyst.md) | STAFF | Front | Head of Execution | `tca-analyst-log.md` |

**Archived 2026-08-19** (operator-authorized cut; never spawned, zero log entries, kept for future
reference rather than deleted — see
[the audit](../notes/audits/2026-08-19-governance-friction-persona-panel-audit.md) and the design
spec's [§6.7 retirement procedure](../superpowers/specs/2026-08-18-loop-persona-hierarchy-design.md#67-persona-retirement-procedure-individual-seat--added-2026-08-19)):
Risk Analyst (Intraday), Model Validation Analyst, Robustness Analyst, Documentation Analyst,
Research Registry Analyst — full charters preserved at
[`docs/personas/archive/`](archive/). Front-office Staff are unaffected and still in active use.
Re-propose any of these (or a new Staff seat in their domain) if a Middle/Back-office STAFF-tier
review is actually needed — same intake-rule discipline GRAND already applies to pursuits (§11).

**Not on this roster:** Head of Engineering's staff are the literal Cursor worker agents dispatched
per packet under the existing `cursor-fleet` skill — ephemeral, not a persistent named persona (see
`head-of-engineering.md`).
