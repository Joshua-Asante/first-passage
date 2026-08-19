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
