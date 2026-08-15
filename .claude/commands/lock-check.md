---
description: Run lock-anchor verifier; surface Closed/Action/Forward routing
allowed-tools: Bash(python scripts/verify_lock_anchors.py:*), Read
---

Run `python scripts/verify_lock_anchors.py` and report the result verbatim.

Then:

- If routing is **Closed**: confirm in one line. No further action.
- If routing is **Action**: unused after the 2026-08-03 params.toml retirement — treat as unexpected; report drifts.
- If routing is **Forward**: state the re-MC trigger that fired (Guardian safe band). Suggest the user review `dd_protection.py` and re-run portfolio_mc if MC inputs changed. Do NOT run portfolio_mc automatically.
- If routing is **Error**: required `dd_protection.py` missing or unparseable — restore and re-run.

Reference: routing semantics defined in [docs/methodology/observation_routing.md](../../docs/methodology/observation_routing.md).
Retired toml hub: [docs/adr/2026-08-03-params-toml-gate-retirement.md](../../docs/adr/2026-08-03-params-toml-gate-retirement.md).
