# `ops/c1_rail/` — listener + sizing host

**Disarmed.** Posture is owned by [`AGENTS.md`](../../AGENTS.md)
§Live-execution posture. Fly standup:
[`deploy/c1_rail/README.md`](../../deploy/c1_rail/README.md)
(standup only — does not authorize arming).

| File | Job |
|---|---|
| `c1_rail_http_server.py` | Listener |
| `c1_sizing_host_reference.py` | Qty / lifecycle / DD compose |
| `c1_rail_arm.py` | Arm / disarm CLI + M1 interlock |
| `c1_rail_telemetry.py` | Event ledger / notifiers |
| `crosstrade_payload.py` | CrossTrade payload |
| `book_*.py`, `account_close_*.py`, `settlement_signing.py` | Track B fixed-book owner, protection, halt, settlement, takeover (offline until deployment GO) |
| `qualification/`, `qualification_cli.py` | Offline fixed-book qualification; `execution/` is the separately installed protected service (see [PIPELINES §P5](../../PIPELINES.md#p5--live-execution-rail-c1--built--currently-disarmed)) |

Paired daemon: [`../c1_signal_daemon/`](../c1_signal_daemon/).
Skill: `.claude/skills/c1-rail/`.
