# `ops/` — operational surface

Imports `core` + root-resident governance. **No strategy is deployed.** Live
posture is owned by [`AGENTS.md`](../AGENTS.md) §Live-execution posture — not
restated here.

| Path | Job |
|---|---|
| [`c1_rail/`](c1_rail/) | `book_policy` and the sizing reference, until S3-4. The rail itself is gone. |
| [`c1_signal_daemon/`](c1_signal_daemon/) | Offline replay library and private port root. The daemon itself is gone. |
| [`contract_roll.py`](contract_roll.py) | 6J and MGC roll calendar and G4 checks |
| [`instruments/`](instruments/) | Per-symbol ledgers + mechanism index |
| [`sentinel/`](sentinel/) | Hygiene / preregistration scans |
| [`cli.py`](cli.py) | Tearsheet-only historical CLI |
| [`prop_envelope_default.md`](prop_envelope_default.md) | Prop-envelope v1 pointer |

See [`REPO_MAP.md`](../REPO_MAP.md) §2.2.

Layer contract: [`REPO_MAP.md`](../REPO_MAP.md).
