"""ic_similarity.py — pairwise near-duplicate report over candidate bar-return series.

Genuinely new, narrowly scoped (2026-08-19): a numeric IC/correlation check
between candidates' MEASURED bar-return series -- RD-Agent(Q)'s "IC >= 0.99
discards a factor" shape -- distinct in kind from the mechanism-family /
instrument concept-dedup that already failed once in this repo and was
retired (docs/adr/2026-08-13-dedup-first-before-new-work.md §3, §5 forbidden
move #1: "a hard, commit-blocking semantic duplicate gate... false-positived
to death"). That prior gate inferred "is this concept already dead" from a
text/label match; this module never does that -- it only computes a
correlation coefficient between two arrays of numbers. Distinct problem,
distinct failure mode, distinct design.

Scope: within ONE mining run's own batch of survivors. register_search.py's
close_run() persists only p-values, never full return series -- there is no
cross-campaign historical corpus of return series anywhere in this repo today,
and building one is a separate, larger, deliberately deferred decision, not
attempted here.

Advisory only, same posture as check_advisor_dedup.py and the 2026-08-13
ADR's own forbidden-move #1 ("stay advisory, always exit 0"): this reports
near-duplicate pairs. It never refuses, blocks, or drops a candidate --
callers decide what (if anything) to do with the report.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

import numpy as np

# RD-Agent(Q)'s own discard threshold (NeurIPS 2025) -- not re-derived here.
DEFAULT_IC_THRESHOLD = 0.99


@dataclass(frozen=True)
class SimilarityFinding:
    candidate_a: str
    candidate_b: str
    correlation: float


def pairwise_similarity_report(
    named_series: Mapping[str, Sequence[float]],
    *,
    threshold: float = DEFAULT_IC_THRESHOLD,
) -> list[SimilarityFinding]:
    """Report (never refuse) candidate pairs whose bar-return series correlate
    at or above ``threshold``.

    All series must be the same length: they are expected to be
    ``RuleEval.bar_returns`` arrays (``discovery.motif_rules.evaluate_rule``),
    which are always full-length and zero-filled where no position is held,
    evaluated against the same underlying series -- so within one run they are
    already index-aligned by construction. Mismatched lengths raise, since a
    correlation across unaligned series would be meaningless, not merely
    imprecise.

    A constant series (a rule with zero variance -- e.g. one that never
    fired) has an undefined correlation with anything; such candidates are
    skipped rather than reported as a spurious 1.0 or NaN, since a rule that
    never fired carries no signal to be redundant with.
    """
    names = list(named_series.keys())
    arrays: dict[str, np.ndarray] = {name: np.asarray(named_series[name], dtype=float) for name in names}
    lengths = {arr.size for arr in arrays.values()}
    if len(lengths) > 1:
        raise ValueError(
            "pairwise_similarity_report requires equal-length, index-aligned "
            f"series; got lengths {sorted(lengths)}"
        )

    findings: list[SimilarityFinding] = []
    for i, a in enumerate(names):
        xa = arrays[a]
        if xa.size == 0 or np.std(xa) == 0.0:
            continue
        for b in names[i + 1 :]:
            xb = arrays[b]
            if xb.size == 0 or np.std(xb) == 0.0:
                continue
            corr = float(np.corrcoef(xa, xb)[0, 1])
            if np.isfinite(corr) and corr >= threshold:
                findings.append(SimilarityFinding(candidate_a=a, candidate_b=b, correlation=corr))
    findings.sort(key=lambda f: -f.correlation)
    return findings
