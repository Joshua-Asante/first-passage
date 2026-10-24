# Q-ORPREM-1 — matched-null opening-range premium (ORB-MNQ-1)

**Status:** ACTIVE — Phase 0 harness built and tested on synthetic data only; pre-registration DRAFT, not ratified; no market data read.

- **Pre-registration:** [`2026-10-19-q-orprem-1-matched-null-prereg-DRAFT.md`](../../../../docs/briefs/pre-registration/2026-10-19-q-orprem-1-matched-null-prereg-DRAFT.md).
- **Engine:** `orb_lib.py` is an LF byte copy of archive `5d47b4dc:lab/analysis/orb/orb_universe_2026-06-22/orb_lib.py`, sha256 `e8b0caf8…5e9259`, marked `-text`. Do not edit it.
- **Harness:** `orprem.py` holds the library. `run_orprem.py` is the `g0`/`score` CLI. Both subcommands refuse (exit 2) until the pre-registration's Status line is FROZEN. `score` also needs the §7 v7 gate.
- **Tests:** `.\fp.ps1 python -m pytest lab/analysis/orb/orprem_mnq_2026-10 -q`. They use synthetic data only.
- **Must run locally:** the inputs are the vendor-licensed TradingView CME exports in the primary checkout. They are never committed.
