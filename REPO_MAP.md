# REPO_MAP — where the code lives

| Path | What it is |
|---|---|
| `core/` | Firm rules (`firm_rules.py`), drawdown protection (`dd_protection.py`), lifecycle, Monte Carlo engine (`mc/`, `portfolio_mc.py`), data loaders, strategy catalog (`strategies/`), canonical CME TradingView exports (`data/`). |
| `lab/` | Research: discovery tooling, analysis campaigns (`analysis/`, each with its own RESULTS), validation utilities, replay. |
| `ops/` | Operations: retired c1 rail and signal daemon (`c1_rail/`, `c1_signal_daemon/`; awaiting removal), instrument profiles, venue editions, calendars. |
| `scripts/` | Launcher (`fp.py`), gate runner (`gate_manifest.py` + `gates.yml`), integrity checks, harness guard hooks, git hooks (`githooks/`). |
| `tests/` | Pytest suites mirroring the layers. |
| `deploy/` | Fly deployment files for the retired c1 hosts. |
| `discovery_manifests/` | Pre-registered search manifests for discovery runs. |
| `docs/` | Docs that code or STATE reads: frozen pre-registrations and spec contracts pinned by lab/ops code, the forward stop rule, the M1 acceptance artifact, the subscription ledger. |

## Layer rule

```text
core imports nothing from other internal layers
lab → core (+ scripts/docs tooling)
ops → core (+ scripts/docs tooling)
lab ↔ ops is forbidden
```

`scripts/check_boundaries.py` enforces this from the layer maps in
`scripts/repo_map_layers.yml`; edit that file to change a classification. Run a
layer module with `fp python -m <module>` from the checkout root.
