# `core/` — locked sink

Imports nothing internal. Human-readable layer contract:
[`REPO_MAP.md`](../REPO_MAP.md). Do not glob this tree to infer live authority.

| Need | Open first |
|---|---|
| Strategy dispositions | [`strategies/CATALOG.md`](strategies/CATALOG.md) |
| Live sizing / DD rule | [`dd_protection.py`](dd_protection.py) · [`firm_rules.py`](firm_rules.py) |
| Lifecycle multiplier | [`lifecycle.py`](lifecycle.py) · [`docs/methodology/strategy_lifecycle.md`](../docs/methodology/strategy_lifecycle.md) |
| MC engine | [`mc/`](mc/) |
| Frozen panels | [`data/`](data/) |

`core/` is an **import root, not a package** — `python -m` needs `PYTHONPATH=core`.
See [`REPO_MAP.md`](../REPO_MAP.md) §2.2.
