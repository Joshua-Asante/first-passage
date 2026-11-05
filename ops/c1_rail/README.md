# `ops/c1_rail/` — listener + sizing host

**Retired 2026-10-29** ([rail ADR addendum](../../docs/adr/2026-07-17-c1-rail-build-account-registration-go.md#addendum-2026-10-29--c1-retired-as-an-execution-route-staged-decommission),
[Stage 1 record](../../docs/adr/2026-07-17-c1-rail-build-account-registration-go.md#stage-1-record--2026-11-03)): nothing here is rebuilt, redeployed, armed or
account-bound; the code stays until the Stage 3 PRs. Posture is owned by
[`AGENTS.md`](../../AGENTS.md) §Live-execution posture. Historical Fly standup:
[`deploy/c1_rail/README.md`](../../deploy/c1_rail/README.md)
(standup only — does not authorize arming).

| File | Job |
|---|---|
| `c1_rail_http_server.py` | Listener |
| `c1_sizing_host_reference.py` | Qty / lifecycle / DD compose |
| `c1_rail_arm.py` | Arm / disarm CLI + M1 interlock |
| `c1_rail_telemetry.py` | Event ledger / notifiers |
| `crosstrade_payload.py` | CrossTrade payload (retired route) |
| `book_*.py`, `account_close_*.py`, `settlement_signing.py` | Track B fixed-book owner, protection, halt, settlement, takeover (retired; offline) |
| `qualification/` | Retired fixed-book qualification modules that rail and daemon tests still consume; the `execution/` service was removed 2026-10-30 (see [PIPELINES §P5](../../PIPELINES.md#p5--python-execution-rail-c1--retired-2026-10-29)) |

Paired daemon: [`../c1_signal_daemon/`](../c1_signal_daemon/).
Skill: `.claude/skills/c1-rail/`.
