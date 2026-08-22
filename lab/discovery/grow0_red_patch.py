"""GROW-0 RED-PATCH: the M-23-shaped attestation control.

Prereg §6.5 (FROZEN, operator GO 2026-08-22) -- standalone, independent of the stochastic
Limb A/B/RED-LEAK/RED-BLIND panels (grow0_harness.py / grow0_scoring.py / grow0_dgp.py). Hand-rolls
the F3 attested pattern inline per the GROW spec's own instruction, since
lab/research_utils/attested_patch.py does not exist yet (F3 spec status: PROPOSED, not built).
"""
from __future__ import annotations

from joblib import Parallel, delayed

_FIRM_KEY = "Tradeify_Select_100K"
_PATCH_KEY = "dd_lock_offset_usd"
_PATCHED_VALUE = 500.0  # any value distinct from the UNREACHABLE default (core/firm_rules.py)
_UNREACHABLE_DEFAULT = 1_000_000.0
_N_WORKERS = 4


def assert_intraday_channel_required(intraday_blocks) -> None:
    """Companion non-vacuity check (prereg §6.5 step 1): a construction-time
    guard proving the GROW-0 lane's own N-SURV-shaped wiring does not silently
    accept clock='eod' (intraday_blocks=None) the way
    prop_survivor_scoring.score_candidate's default path does (that gap is
    named, not modified -- prop_survivor_scoring.py is locked production code).
    """
    if intraday_blocks is None:
        raise ValueError(
            "grow0 N-SURV wrapper requires intraday_blocks; clock='eod' construction is refused"
        )


def _worker_read_patch_target():
    """Runs in a fanned-out worker process under joblib's 'processes' backend.
    Each worker re-imports firm_rules fresh, so it reads whatever value THAT
    process's own import resolved -- not necessarily the parent's runtime patch
    (the M-23 shape).
    """
    from firm_rules import FIRM_RULES

    return FIRM_RULES[_FIRM_KEY][_PATCH_KEY]


def reproduce_m23_parent_only_patch() -> list:
    """Patches FIRM_RULES in the PARENT process only, fans out _N_WORKERS via
    joblib (processes backend), and collects each worker's own read of the
    same key. Returns the list of attestations (restores the original value
    before returning, success or failure).
    """
    from firm_rules import FIRM_RULES

    FIRM_RULES[_FIRM_KEY][_PATCH_KEY] = _PATCHED_VALUE
    try:
        attestations = Parallel(n_jobs=_N_WORKERS, prefer="processes")(
            delayed(_worker_read_patch_target)() for _ in range(_N_WORKERS)
        )
    finally:
        FIRM_RULES[_FIRM_KEY][_PATCH_KEY] = _UNREACHABLE_DEFAULT
    return list(attestations)


def assert_singleton_attestation(attestations, expected) -> None:
    """Hand-rolled equivalent of the pending F3
    attested_patch.assert_singleton_attestation primitive."""
    distinct = set(attestations)
    if distinct != {expected}:
        raise AssertionError(
            f"non-singleton attested set (the M-23 shape): got {distinct}, "
            f"expected {{{expected}}}"
        )


def run_red_patch() -> str:
    """Prereg §6.5 steps 1-4, combined. Returns FAILED_AS_EXPECTED iff the M-23
    bug reproduces (workers do not see the parent's patch) AND the attestation
    guard correctly raises on that non-singleton set.
    """
    try:
        assert_intraday_channel_required(None)
    except ValueError:
        pass
    else:
        raise AssertionError("companion non-vacuity check did not raise on intraday_blocks=None")

    attestations = reproduce_m23_parent_only_patch()
    if set(attestations) == {_PATCHED_VALUE}:
        return "PASSED_UNEXPECTEDLY"  # bug did not reproduce -- nothing for the guard to catch

    try:
        assert_singleton_attestation(attestations, _PATCHED_VALUE)
    except AssertionError:
        return "FAILED_AS_EXPECTED"
    return "PASSED_UNEXPECTEDLY"  # guard should have raised and didn't
