"""Normalized instrument cost model for discovery campaigns.

Parameterized reproduction of the two cost laws found across the corpus
(``edge/hurdle_4x`` in bp-of-notional, and ``edge/mean_cost_R`` in R of
opening-range points), with explicit ``slip_convention`` and required
``firm_key``.

This module does NOT supersede the frozen per-campaign ``cost_*.py`` files
(``cost_mnq.py``, ``cost_es.py``, ``cost_mgc.py``). Those remain the citable
basis for their closed verdicts; figures published under them are not moved
by anything here. Use this module for new work and for re-deriving a campaign
figure from that campaign's own declared primitives.

Instrument specs are sourced to
``.claude/skills/databento-data/reference/proxy-discipline.md`` (MYM
``tick_size`` = 1.00 index point — not MNQ's 0.25). Parent + energy rows
extend that table for campaigns that score on parent/NG notionals.

No R↔bp conversion exists: R normalizes by opening-range points, bp by
notional; refuse cross-unit comparison.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Literal, Sequence

try:
    from firm_rules import FIRM_RULES
except ImportError:  # pragma: no cover
    from core.firm_rules import FIRM_RULES

SlipConvention = Literal["per_side", "total_rt"]
SLIP_CONVENTIONS: frozenset[str] = frozenset({"per_side", "total_rt"})

COST_LAW_MULTIPLE = 4.0
BP_PER_UNIT = 10_000.0

# FIRM_RULES[firm_key]["cost_per_side_usd"] is the index-micro all-in row.
# Applying it to products without a row is the rates_ev_zf_recon defect shape.
INDEX_MICRO_COMMISSION_INSTRUMENTS: frozenset[str] = frozenset(
    {"MES", "MNQ", "MYM", "M2K"}
)
NO_COMMISSION_ROW_INSTRUMENTS: frozenset[str] = frozenset(
    {
        "ZN",
        "ZB",
        "ZF",
        "CL",
        "NG",
        "6E",
        # SPECS keys that already raise via the catch-all — named so the
        # closed-world partition cannot drift again (SSOT Phase 3).
        "MGC",
        "ES",
        "NQ",
        "YM",
        "RTY",
        "GC",
        "MNG",
    }
)


@dataclass(frozen=True)
class InstrumentSpec:
    symbol: str
    multiplier: float
    tick_size: float
    tick_value: float


# Sourced to proxy-discipline.md (+ standard CME parent/energy specs for
# campaigns that score on those notionals). MYM tick_size = 1.00.
INSTRUMENT_SPECS: dict[str, InstrumentSpec] = {
    "MES": InstrumentSpec("MES", 5.0, 0.25, 1.25),
    "MNQ": InstrumentSpec("MNQ", 2.0, 0.25, 0.50),
    "MYM": InstrumentSpec("MYM", 0.50, 1.0, 0.50),
    "M2K": InstrumentSpec("M2K", 5.0, 0.10, 0.50),
    "MGC": InstrumentSpec("MGC", 10.0, 0.10, 1.00),
    "ES": InstrumentSpec("ES", 50.0, 0.25, 12.50),
    "NQ": InstrumentSpec("NQ", 20.0, 0.25, 5.00),
    "YM": InstrumentSpec("YM", 5.0, 1.0, 5.00),
    "RTY": InstrumentSpec("RTY", 50.0, 0.10, 5.00),
    "GC": InstrumentSpec("GC", 100.0, 0.10, 10.00),
    "NG": InstrumentSpec("NG", 10_000.0, 0.001, 10.00),
    "MNG": InstrumentSpec("MNG", 1_000.0, 0.001, 1.00),
}


@dataclass(frozen=True)
class BpCostResult:
    instrument: str
    firm_key: str
    price: float
    commission_per_side_usd: float
    slip_ticks: float
    slip_convention: SlipConvention
    slip_rt_usd: float
    slip_rt_pt: float
    rt_cost_usd: float
    notional_usd: float
    hurdle_1x_frac: float
    hurdle_4x_frac: float
    hurdle_4x_bp: float
    ratio_convention: str = "edge_over_hurdle_4x"


@dataclass(frozen=True)
class RCostResult:
    instrument: str
    firm_key: str
    commission_per_side_usd: float
    slip_ticks: float
    slip_convention: SlipConvention
    rt_pt: float
    mean_cost_R: float
    n_ranges: int
    ratio_convention: str = "edge_over_mean_cost_R"


def _spec(instrument: str) -> InstrumentSpec:
    try:
        return INSTRUMENT_SPECS[instrument]
    except KeyError as exc:
        raise ValueError(
            f"unknown instrument {instrument!r}; known: "
            f"{sorted(INSTRUMENT_SPECS)}"
        ) from exc


def _require_slip_convention(slip_convention: str) -> SlipConvention:
    if slip_convention not in SLIP_CONVENTIONS:
        raise ValueError(
            f"slip_convention must be one of {sorted(SLIP_CONVENTIONS)}, "
            f"got {slip_convention!r}"
        )
    return slip_convention  # type: ignore[return-value]


def closed_world_findings() -> list[str]:
    """Intra-module partition: every SPECS key is classified; every priced
    index-micro has a spec; the two commission sets are disjoint.

    Does not join ``ops/instruments`` ledgers (many are unpriced by design).
    """
    specs = set(INSTRUMENT_SPECS)
    index_micro = set(INDEX_MICRO_COMMISSION_INSTRUMENTS)
    no_row = set(NO_COMMISSION_ROW_INSTRUMENTS)
    findings: list[str] = []
    missing_specs = sorted(index_micro - specs)
    if missing_specs:
        findings.append(
            "INDEX_MICRO_COMMISSION_INSTRUMENTS notsubseteq INSTRUMENT_SPECS: "
            + ", ".join(missing_specs)
        )
    unclassified = sorted(specs - index_micro - no_row)
    if unclassified:
        findings.append(
            "INSTRUMENT_SPECS key(s) in neither INDEX_MICRO nor "
            "NO_COMMISSION: " + ", ".join(unclassified)
        )
    overlap = sorted(index_micro & no_row)
    if overlap:
        findings.append(
            "INDEX_MICRO intersect NO_COMMISSION nonempty: "
            + ", ".join(overlap)
        )
    return findings


def resolve_commission(firm_key: str, instrument: str) -> float:
    """Resolve ``cost_per_side_usd`` from ``FIRM_RULES``.

    ``firm_key`` is required (no default). Instruments without a commission
    row at the firm (ZN/ZB/ZF/CL/NG/full-size 6E, and any non-index-micro)
    raise naming the gap — never substitute the index-micro rate.

    Traceability (claim-alignment M40): BluSky rows encode 0.95 as an
    NT-schedule proxy — not venue-published Evaluation ($0.50 Rithmic-class;
    funded unpublished). Do not treat as venue-published in F3 EV/$ rankings
    until O-G directs a change.
    """
    if firm_key not in FIRM_RULES:
        raise KeyError(
            f"unknown firm_key {firm_key!r}; not in FIRM_RULES"
        )
    if instrument in NO_COMMISSION_ROW_INSTRUMENTS or (
        instrument not in INDEX_MICRO_COMMISSION_INSTRUMENTS
    ):
        raise ValueError(
            f"no commission row for {instrument} at {firm_key}: "
            f"FIRM_RULES cost_per_side_usd is the index-micro row only; "
            f"do not substitute it for {instrument}"
        )
    cps = FIRM_RULES[firm_key].get("cost_per_side_usd")
    if cps is None:
        raise ValueError(
            f"{firm_key!r} has no cost_per_side_usd "
            f"(cannot price {instrument})"
        )
    return float(cps)


def _commission(
    firm_key: str,
    instrument: str,
    commission_per_side: float | None,
) -> float:
    if firm_key not in FIRM_RULES:
        raise KeyError(
            f"unknown firm_key {firm_key!r}; not in FIRM_RULES"
        )
    if commission_per_side is not None:
        return float(commission_per_side)
    return resolve_commission(firm_key, instrument)


def slip_rt_usd(
    instrument: str,
    *,
    slip_ticks: float,
    slip_convention: str,
) -> float:
    """Round-trip slippage dollars under the declared convention."""
    spec = _spec(instrument)
    conv = _require_slip_convention(slip_convention)
    if conv == "per_side":
        return 2.0 * slip_ticks * spec.tick_value
    return slip_ticks * spec.tick_value


def rt_cost_usd(
    instrument: str,
    *,
    commission_per_side: float,
    slip_ticks: float,
    slip_convention: str,
) -> float:
    """Round-trip $ cost: commission + slip under ``slip_convention``.

    ``per_side``: ``2 * (commission + slip_ticks * tick_value)``
    ``total_rt``: ``2 * commission + slip_ticks * tick_value``
      (``cost_es.py`` passive model — slip is for the WHOLE round trip).
    """
    conv = _require_slip_convention(slip_convention)
    spec = _spec(instrument)
    if conv == "per_side":
        return 2.0 * (commission_per_side + slip_ticks * spec.tick_value)
    return 2.0 * commission_per_side + slip_ticks * spec.tick_value


def bp_hurdle(
    instrument: str,
    price: float,
    *,
    firm_key: str,
    slip_ticks: float,
    slip_convention: str,
    commission_per_side: float | None = None,
) -> BpCostResult:
    """4× RT cost as bp of notional.

    ``hurdle_4x = 4 * rt_usd / (price * multiplier)`` expressed in bp.
    ``firm_key`` and ``slip_convention`` are required (no defaults).
    Pass ``commission_per_side`` to reproduce a campaign's declared
    commission; omit it to resolve through ``FIRM_RULES``.
    """
    conv = _require_slip_convention(slip_convention)
    spec = _spec(instrument)
    cps = _commission(firm_key, instrument, commission_per_side)
    slip_usd = slip_rt_usd(
        instrument, slip_ticks=slip_ticks, slip_convention=conv
    )
    rt = rt_cost_usd(
        instrument,
        commission_per_side=cps,
        slip_ticks=slip_ticks,
        slip_convention=conv,
    )
    notional = price * spec.multiplier
    frac = rt / notional if notional > 0 else float("inf")
    return BpCostResult(
        instrument=instrument,
        firm_key=firm_key,
        price=price,
        commission_per_side_usd=cps,
        slip_ticks=slip_ticks,
        slip_convention=conv,
        slip_rt_usd=slip_usd,
        slip_rt_pt=slip_usd / spec.multiplier,
        rt_cost_usd=rt,
        notional_usd=notional,
        hurdle_1x_frac=frac,
        hurdle_4x_frac=COST_LAW_MULTIPLE * frac,
        hurdle_4x_bp=COST_LAW_MULTIPLE * frac * BP_PER_UNIT,
    )


def r_hurdle(
    instrument: str,
    or_ranges: Sequence[float] | Iterable[float],
    *,
    firm_key: str,
    slip_ticks: float,
    slip_convention: str,
    commission_per_side: float | None = None,
) -> RCostResult:
    """Mean-of-ratios R cost: ``mean(rt_pt / or_range_i)``.

    NOT ``rt_pt / median(range)`` — that wrong form understates by ~21% on
    the ORB-MNQ panel. ``firm_key`` and ``slip_convention`` required.
    """
    conv = _require_slip_convention(slip_convention)
    spec = _spec(instrument)
    cps = _commission(firm_key, instrument, commission_per_side)
    rt = rt_cost_usd(
        instrument,
        commission_per_side=cps,
        slip_ticks=slip_ticks,
        slip_convention=conv,
    )
    rt_pt = rt / spec.multiplier
    ranges = [float(r) for r in or_ranges]
    if not ranges:
        raise ValueError("or_ranges must be non-empty")
    if any(r <= 0 for r in ranges):
        raise ValueError("or_ranges must be strictly positive")
    mean_cost_R = sum(rt_pt / r for r in ranges) / len(ranges)
    return RCostResult(
        instrument=instrument,
        firm_key=firm_key,
        commission_per_side_usd=cps,
        slip_ticks=slip_ticks,
        slip_convention=conv,
        rt_pt=rt_pt,
        mean_cost_R=mean_cost_R,
        n_ranges=len(ranges),
    )


def convert_r_to_bp(*_args, **_kwargs) -> float:
    """No R↔bp conversion exists — raise rather than invent one."""
    raise ValueError(
        "No R↔bp conversion exists: R normalizes by opening-range points, "
        "bp by notional. Refuse cross-unit comparison."
    )
