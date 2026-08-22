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

Per-script layer classification (governance vs lab vs ops) lives in
[`REPO_MAP.md`](../REPO_MAP.md) §2.1 and must stay mirrored in
`check_boundaries.py`'s `SCRIPTS_LAYER`.
