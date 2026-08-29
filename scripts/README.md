# `scripts/` — gates and discipline CLIs

Composition authority is [`gates.yml`](gates.yml) via
[`gate_manifest.py`](gate_manifest.py)
([W5 ADR](../docs/adr/2026-08-07-w5-governance-diet.md)).
Do not hand-maintain a parallel list.

```text
python scripts/gate_manifest.py --list
make check          # same runner, check tier
make validate       # data manifests + pine
```

Install hooks once per clone: `bash scripts/install_hooks.sh`.

Per-script layer classification is owned by
`check_boundaries.py`'s `SCRIPTS_LAYER` (fallback **governance**). The
human-readable table in [`REPO_MAP.md`](../REPO_MAP.md) §2.1 is generated
from that dict + [`gates.yml`](gates.yml) + `git ls-files 'scripts/*.py'`:

```text
python scripts/check_repo_map_scripts_table.py --write
python scripts/check_repo_map_scripts_table.py --check
```

Do not hand-edit the table. `--check` is not wired into `gates.yml`.
