# `lab/analysis/` — hot campaign bodies + archive stubs

**Open [`../CATALOG.md`](../CATALOG.md) first.** Do not glob this directory
to infer what is live.

| Layout | Meaning |
|---|---|
| `<theme>/<slug>/` | Hot body (theme README names the family) |
| `<slug>/CARD.md` | Archived stub; body is `lab/archive/<slug>/` |
| `_inbox/` | Unassigned — must leave before archive |

Theme READMEs today: `c1/`, `harvest/`, `regime/`, `striker/`, `aegis/`,
`orb/`, `legacy/`, `mc/`, `_inbox/`.
Archive tool: `python scripts/archive_lab_analysis.py --help`.
