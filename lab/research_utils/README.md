# `lab/research_utils/` — stable research primitives

W4: SPA/StepM/PBO are **dormant**; DSR remains callable. Live admission
floor is G0–G5+G8. Do not reimplement dormant library calls.
Owner: [`docs/adr/2026-08-07-w4-minimal-gate-set-dormancy.md`](../../docs/adr/2026-08-07-w4-minimal-gate-set-dormancy.md).

Import root is `lab/` (`from research_utils.repo_root import repo_root`).
Camp-local siblings: [`camp_import.py`](camp_import.py).
