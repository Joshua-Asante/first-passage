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
| [Risk Analyst (Intraday)](risk-analyst-intraday.md) | STAFF | Middle | Head of Risk & Sizing | `risk-analyst-intraday-log.md` |
| [Model Validation Analyst](model-validation-analyst.md) | STAFF | Middle | Head of Validation | `model-validation-analyst-log.md` |
| [Robustness Analyst](robustness-analyst.md) | STAFF | Middle | Head of Validation | `robustness-analyst-log.md` |
| [Documentation Analyst](documentation-analyst.md) | STAFF | Back | Head of Governance | `documentation-analyst-log.md` |
| [Research Registry Analyst](research-registry-analyst.md) | STAFF | Back | Head of Governance | `research-registry-analyst-log.md` |

**Not on this roster:** Head of Engineering's staff are the literal Cursor worker agents dispatched
per packet under the existing `cursor-fleet` skill — ephemeral, not a persistent named persona (see
`head-of-engineering.md`).
