# `ops/` — operational surface

Imports `core` + root-resident governance. **No strategy is deployed.** Live
posture is owned by [`CLAUDE.md`](../CLAUDE.md) §Live-execution posture — not
restated here.

| Path | Job |
|---|---|
| [`c1_rail/`](c1_rail/) | Listener / sizing host / arm CLI (disarmed) |
| [`c1_signal_daemon/`](c1_signal_daemon/) | S2b signal daemon (`emit_enabled=false`) |
| [`instruments/`](instruments/) | Per-symbol ledgers + mechanism index |
| [`sentinel/`](sentinel/) | Hygiene / preregistration scans |
| [`recall/`](recall/) | Recall-sidecar guard |
| [`cli.py`](cli.py) | Tearsheet-only historical CLI |
| [`prop_envelope_default.md`](prop_envelope_default.md) | Prop-envelope v1 pointer |

Import split: rail modules are **flat** (`c1_rail_arm`, … under
`PYTHONPATH=ops/c1_rail`); the daemon is a **package**
(`python -m c1_signal_daemon` under `PYTHONPATH=ops/c1_signal_daemon`).
See [`REPO_MAP.md`](../REPO_MAP.md) §2.2.

Deploy packaging: [`deploy/c1_rail/`](../deploy/c1_rail/) ·
[`deploy/c1_signal_daemon/`](../deploy/c1_signal_daemon/).
Layer contract: [`REPO_MAP.md`](../REPO_MAP.md).
