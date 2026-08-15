"""Compatibility facade and CLI entrypoint for :mod:`mc`.

Implementation ownership:
  * ``mc.ingest`` — TradingView ingestion and panel construction
  * ``mc.simulation`` — deterministic paths and seeded bootstrap
  * ``mc.modes`` — configurations, reporting, orchestration, and CLI modes
"""

from __future__ import annotations

try:
    from .mc import modes as _modes
except ImportError:
    from mc import modes as _modes


# Preserve every historical import, including intentionally private helpers
# used by pinned research scripts. New code should import focused modules.
for _name in dir(_modes):
    if not _name.startswith("__"):
        globals()[_name] = getattr(_modes, _name)

del _name


def _run_seeds(
    blocks,
    effective_trigger,
    dd_scale,
    seeds=_modes.SEEDS,
    parallel=False,
    strats=_modes.STRATS,
    *,
    firm_kwargs=None,
):
    """Forward facade-owned simulation count to the focused implementation."""
    return _modes._run_seeds(
        blocks,
        effective_trigger,
        dd_scale,
        seeds=seeds,
        parallel=parallel,
        strats=strats,
        firm_kwargs=firm_kwargs,
        sims_per_seed=SIMS_PER_SEED,
    )


if __name__ == "__main__":
    _modes.main()
