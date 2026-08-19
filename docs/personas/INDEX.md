# Persona Roster — Index

One row per persona defined under `docs/personas/`. See the
[design spec](../superpowers/specs/2026-08-18-loop-persona-hierarchy-design.md) for the full
architecture, panel mechanics, and independence rules this roster implements.

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
