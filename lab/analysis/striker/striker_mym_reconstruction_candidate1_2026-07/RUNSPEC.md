# S-MYM-ORC-02 development runspec

Authority: [`2026-07-16-striker-mym-reconstruction-candidate-2-prereg.md`](../../../docs/briefs/pre-registration/2026-07-16-striker-mym-reconstruction-candidate-2-prereg.md), status `FROZEN`.

Machine contract: [`runspec.json`](runspec.json)

Canonical `runspec.json` SHA256:

```text
a55a6b5d9eab85800a9cd33f25b6ae10410a4f0d19ad29985ec8bf9840843d0d
```

The JSON freezes the complete §2 candidate, the development-only D0–D9 gates, panel identity and integrity expectations, development date ceiling, placebo anchors, cost model, output paths, and statistical constants. D5 derives its block size with `lab.research_utils.universe_gate.acf_block_size(net_R)` and then uses the existing Politis–Romano stationary bootstrap for 10,000 samples at seed 42.

Candidate #2 binds cumulative `K_reconstruction=2` and the frozen session calendar [`session_calendar.json`](session_calendar.json), SHA256 `7ff65ef4b0bdceb620f077708e55075f5f4295ae6fd594a56595282e72a8a3bd`. The 53 allowlisted dates use their exact mapped 12:45/13:00 ET force-flat fill; all other eligible sessions use the standard 16:00 ET fill. Every trigger is exactly one 15-minute bar earlier. Dynamic last-bar inference is forbidden.

The full panel may be integrity-checked, but candidate simulation is restricted to `2020-07-01..2023-12-31`. The reserved holdout dates are metadata only: this contract contains no holdout execution command or holdout output path.

Cost accounting is $0.91 commission plus one $0.50 tick, totaling **$1.41 per contract per filled side**. The R denominator is the actual integer-sized initial risk:

```text
base_qty × stop_points × $0.50
```

Expected development outputs, generated only when the operator authorizes the real development P&L run:

- `development_trades.csv`
- `development_events.csv`
- `development_metrics.json`
- `placebo_results.json`
- `DEVELOPMENT_RESULTS.md`
- `artifact_manifest.json` (hashes the five outputs above; never self-hashes)
