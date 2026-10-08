"""Prop survivor-scoring harness — G0–G8 scorecard over the four frozen $100K tiers.

Faithful transcription of
``docs/briefs/pre-registration/2026-08-26-prop-survivor-scoring-prereg-v2.md``
(v2 — Part A eval ceiling 5.0%, operator risk-tolerance override, 2026-08-26;
supersedes the 2026-07-13 v1 at 3.0%, closed not edited per Trap #12 — see v2
§8 for the full disclosed rationale) into executable code. Ceiling numbers,
tier names, seeds, and sim counts are **parsed from the pre-registration**
(never hardcoded in gate logic).

Build-ahead-of-candidate: no DISC-CAMP-0 survivor exists; callers feed synthetic
or future-campaign ``candidate_daily_pnl`` arrays. This module does not switch
``ACTIVE_FIRM``, edit ``FIRM_RULES``, or read ``compute_default_config()['bust_rate']``.

Import contract: ``lab → core`` only (never ``ops``).
"""
from __future__ import annotations

import json
import re
import warnings
from dataclasses import asdict, dataclass, field
from pathlib import Path
import inspect
from typing import Literal, Mapping, Sequence

import numpy as np
import pandas as pd

try:  # dual-import: package path or flat PYTHONPATH=lab + core/
    from dd_protection import DD_SCALE
    from firm_rules import FIRM_RULES
    from mc.ingest import build_week_blocks
    from mc.preflight import assert_engine_ready, firm_kwargs, summarize_outcomes
    from mc.simulation import HORIZON_CAP, run_seed
except ImportError:  # pragma: no cover
    from core.dd_protection import DD_SCALE
    from core.firm_rules import FIRM_RULES
    from core.mc.ingest import build_week_blocks
    from core.mc.preflight import assert_engine_ready, firm_kwargs, summarize_outcomes
    from core.mc.simulation import HORIZON_CAP, run_seed

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PREREG = (
    REPO_ROOT
    / "docs"
    / "briefs"
    / "pre-registration"
    / "2026-08-26-prop-survivor-scoring-prereg-v2.md"
)


class StaleGateWarning(UserWarning):
    """Gate numbers were parsed from a CLOSED / superseded pre-registration.

    A pre-registration is immutable and is never deleted when superseded — it is the
    audit record proving a ceiling change was an open, dated override rather than a
    quiet edit. That permanence means a superseded file stays parseable forever, so an
    explicit ``path=`` can hand back a dead gate silently. This warns instead.
    """


# Prior-art idiom (tradeify remc / pre-reg §7 item 6): dd_protection OFF for scoring.
# Named here as the mechanism constant, not a ceiling — ceiling numbers live in
# ScoringThresholds loaded from the pre-reg. DD_SCALE imported from dd_protection.
NO_PROTECTION_TRIGGER = 10.0
CANDIDATE_STRAT = ("candidate",)

EnvelopeVerdict = Literal["YES", "NO"]


@dataclass(frozen=True)
class ScoringThresholds:
    """Frozen gate numbers + run posture, parsed from the pre-registration."""

    eval_bust_ceiling: float
    funded_bust_ceiling: float
    pass_floor: float
    tier_keys: tuple[str, ...]
    seeds: tuple[int, ...]
    sims_per_seed: int
    horizon: int
    cost_law_multiple: float
    source_path: str
    #: Non-None when the parsed pre-registration's own Status line says it is CLOSED
    #: or superseded — i.e. these numbers are a historical record, not the live gate.
    #: Carries the Status text verbatim so a caller can print it. See
    #: ``load_scoring_thresholds``; anchor incident 2026-09-02 (a retrieved harness
    #: silently scored against the superseded 3.0% ceiling a week after it was raised).
    superseded_note: str | None = None

    @property
    def is_superseded(self) -> bool:
        """True when these numbers came from a closed/superseded pre-registration."""
        return self.superseded_note is not None

    @property
    def trailing_locking_tiers(self) -> frozenset[str]:
        return frozenset(
            t
            for t in self.tier_keys
            if FIRM_RULES[t].get("dd_type") == "trailing_locking"
        )


@dataclass(frozen=True)
class G1Result:
    r_deploy: int
    expectancy_ratio: float
    deployable_default_envelope: EnvelopeVerdict
    halted: bool


@dataclass(frozen=True)
class G2Result:
    firm_key: str
    cost_per_side_usd: float
    rt_cost_usd: float
    hurdle_usd: float
    gross_edge_usd: float
    passed: bool


@dataclass(frozen=True)
class TierScore:
    firm_key: str
    dd_type: str
    f2_label: str | None
    g3_ok: bool
    run1: dict
    run2: dict
    clears_part_a: bool
    clears_funded: bool
    gated_on: str  # "run2" | "run1_degenerate"


@dataclass(frozen=True)
class TierSeries:
    """One firm tier's own daily series (four-firm re-MC prereg I-19, step 2(c)).

    ``daily_pnl`` is the series netted at that tier's own cost; ``intraday_low`` is
    its paired per-day excursion (<= 0). ``protected_pnl``/``protected_low`` are the
    optional mode-switching twins (prereg I-17), given together or not at all.
    """

    daily_pnl: np.ndarray
    intraday_low: np.ndarray | None = None
    protected_pnl: np.ndarray | None = None
    protected_low: np.ndarray | None = None


def _mode_switching_supported() -> bool:
    """True once the kernel's mode-switching keywords exist (PR #708).

    Read from ``run_seed`` (the kernel), not ``run_tier_remc``, so a wrapper or test
    spy around ``run_tier_remc`` cannot change the answer.
    """
    return "protected_blocks" in inspect.signature(run_seed).parameters


def _tier_blocks(
    tier_series: Mapping[str, TierSeries],
    tier_keys: Sequence[str],
    mode_trigger: float | None,
) -> tuple[dict[str, dict], bool]:
    """Validate the per-tier mapping (fail closed) and pair each tier's blocks."""
    if set(tier_series) != set(tier_keys):
        raise ValueError(
            "tier_series must hold every tier and only those: expected "
            f"{sorted(tier_keys)}, got {sorted(tier_series)}"
        )
    entries = [tier_series[k] for k in tier_keys]
    # Every supplied channel, on every tier, must have the same length BEFORE any
    # week-blocking: blocking drops incomplete final weeks, so a mismatch would
    # otherwise be silently truncated away (Codex 4190889391).
    lengths = {
        len(channel)
        for e in entries
        for channel in (e.daily_pnl, e.intraday_low, e.protected_pnl, e.protected_low)
        if channel is not None
    }
    if len(lengths) != 1:
        raise ValueError(
            f"every tier's channels must all be the same length, got {sorted(lengths)}"
        )
    has_low = {e.intraday_low is not None for e in entries}
    if len(has_low) != 1:
        raise ValueError("intraday_low must be given for every tier or for none")
    protected = {(e.protected_pnl is not None, e.protected_low is not None) for e in entries}
    if len(protected) != 1:
        raise ValueError("protected channels must be given for every tier or for none")
    has_protected, has_protected_low = protected.pop()
    if has_protected != has_protected_low:
        raise ValueError("protected_pnl and protected_low are given together")
    if has_protected and has_low != {True}:
        raise ValueError("protected channels require intraday_low on every tier (prereg I-12)")
    if has_protected and mode_trigger is None:
        raise ValueError("protected channels require mode_trigger")
    if mode_trigger is not None and not has_protected:
        raise ValueError("mode_trigger requires protected channels for every tier")
    if has_protected and not _mode_switching_supported():
        raise ValueError(
            "mode-switching inputs given but the kernel lacks mode-switching (PR #708 not "
            "merged); per prereg I-17 the fallback runs normal-only inputs, never a silent drop"
        )
    out: dict[str, dict] = {}
    for key, entry in zip(tier_keys, entries):
        if entry.intraday_low is not None:
            blocks, lows = paired_blocks_from_daily(entry.daily_pnl, entry.intraday_low)
        else:
            blocks, lows = blocks_from_daily_pnl(entry.daily_pnl), None
        tier = {"blocks": blocks, "intraday_blocks": lows}
        if has_protected:
            p_blocks, p_lows = paired_blocks_from_daily(entry.protected_pnl, entry.protected_low)
            tier.update(protected_blocks=p_blocks, protected_intraday_blocks=p_lows,
                        mode_trigger=mode_trigger)
        out[key] = tier
    return out, has_low == {True}


@dataclass
class ScoringReport:
    strategy_label: str
    g1: G1Result
    g2_by_tier: dict[str, G2Result] = field(default_factory=dict)
    tiers: dict[str, TierScore] = field(default_factory=dict)
    routing: str = "STANDALONE"
    funded_ruin_tier_count: int = 0
    discharges_falsifier: bool = False
    halted_at: str | None = None
    thresholds_source: str = ""
    regime_robustness_gate: str = (
        "TODO — deferred per handoff §0.5(D); run before trusting a real-candidate ceiling"
    )
    # O-4 Slice A (operator ruling 2026-10-02, prereg I-12): which breach clock the
    # tier reads used, and whether the read may GATE a clear. EOD-clock reads are
    # reportable, never gating; an intraday-honest read gates only when no gating
    # tier's channel was vacuous. Set on every return path of ``score_candidate``.
    breach_clock: str = "eod"
    gate_grade: bool = False
    gate_grade_reasons: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "strategy_label": self.strategy_label,
            "g1": asdict(self.g1),
            "g2_by_tier": {k: asdict(v) for k, v in self.g2_by_tier.items()},
            "tiers": {k: asdict(v) for k, v in self.tiers.items()},
            "routing": self.routing,
            "funded_ruin_tier_count": self.funded_ruin_tier_count,
            "discharges_falsifier": self.discharges_falsifier,
            "halted_at": self.halted_at,
            "thresholds_source": self.thresholds_source,
            "regime_robustness_gate": self.regime_robustness_gate,
            "breach_clock": self.breach_clock,
            "gate_grade": self.gate_grade,
            "gate_grade_reasons": list(self.gate_grade_reasons),
        }

    def write_json(self, path: Path | str) -> None:
        Path(path).write_text(json.dumps(self.to_dict(), indent=2) + "\n", encoding="utf-8")


def load_scoring_thresholds(
    path: Path | str | None = None,
) -> ScoringThresholds:
    """Parse frozen ceiling / tiers / seeds from the survivor-scoring pre-reg.

    Refuses to guess — any missing number raises ``ValueError``.
    """
    prereg = Path(path) if path is not None else DEFAULT_PREREG
    text = prereg.read_text(encoding="utf-8")

    def _req(pattern: str, label: str) -> str:
        m = re.search(pattern, text)
        if not m:
            raise ValueError(
                f"pre-registration {prereg} has no parseable {label}; "
                f"refusing to guess a default."
            )
        return m.group(1)

    eval_bust = float(
        _req(
            r"headline\s+\*\*bust\s*[≤<=]\s*([0-9]*\.?[0-9]+)\s*%",
            "eval bust ceiling (Part A)",
        )
    )
    funded_bust = float(
        _req(
            r"funded ruin ceiling:\*\*\s+\*\*bust\s*[≤<=]\s*([0-9]*\.?[0-9]+)\s*%",
            "funded bust ceiling (Part B)",
        )
    )
    # Prefer the explicit P(pass) ≥ 50% form; fall back to bare "pass floor … 50%".
    pass_m = re.search(
        r"P\(pass\)\s*[≥>=]\s*([0-9]*\.?[0-9]+)\s*%",
        text,
    ) or re.search(
        r"pass floor[^\n]*?([0-9]*\.?[0-9]+)\s*%",
        text,
        re.IGNORECASE,
    )
    if not pass_m:
        raise ValueError(
            f"pre-registration {prereg} has no parseable pass floor; refusing to guess."
        )
    pass_floor = float(pass_m.group(1))

    tier_m = re.search(
        r"`(Bulenox_100K)`\s*[·•]\s*`?(Tradeify_Select_100K)`?\s*[·•]\s*"
        r"`?(MFFU_Rapid_100K)`?\s*[·•]\s*`?(BluSky_Premium_100K)`?",
        text,
    )
    if not tier_m:
        # Looser: require all four names present in order of first appearance in §3.
        needed = (
            "Bulenox_100K",
            "Tradeify_Select_100K",
            "MFFU_Rapid_100K",
            "BluSky_Premium_100K",
        )
        positions = []
        for name in needed:
            idx = text.find(name)
            if idx < 0:
                raise ValueError(
                    f"pre-registration {prereg} missing frozen tier {name!r}."
                )
            positions.append((idx, name))
        positions.sort()
        tier_keys = tuple(n for _, n in positions)
        # Sanity: §3 cross-section sentence should contain all four close together.
        if tier_keys != needed:
            # Still accept if all four exist; order from first-appearance is fine.
            pass
    else:
        tier_keys = tuple(tier_m.group(i) for i in range(1, 5))

    seeds_m = re.search(
        r"seeds\s+\*\*(\d+)\s*/\s*(\d+)\s*/\s*(\d+)\*\*",
        text,
        re.IGNORECASE,
    ) or re.search(
        r"seeds\s+(\d+)\s*/\s*(\d+)\s*/\s*(\d+)",
        text,
        re.IGNORECASE,
    )
    if not seeds_m:
        raise ValueError(f"pre-registration {prereg} has no parseable seeds 42/123/2026.")
    seeds = tuple(int(seeds_m.group(i)) for i in range(1, 4))

    sims_m = re.search(
        r"\*\*([0-9][0-9,]*)\s*[kK]?\s*[×x]\s*3\s*seeds",
        text,
    ) or re.search(
        r"([0-9][0-9,]*)\s*[kK]?\s*[×x]\s*3\s*seeds",
        text,
    )
    if not sims_m:
        raise ValueError(f"pre-registration {prereg} has no parseable 10k × 3 seeds count.")
    sims_raw = sims_m.group(1).replace(",", "")
    # "10k" form in the pre-reg §2 G4 line — multiply when a k/K follows the digits.
    sims_span = sims_m.group(0)
    sims_per_seed = int(sims_raw) * (1000 if re.search(r"\d\s*[kK]", sims_span) else 1)

    horizon_m = re.search(
        r"horizon\s+\*\*(\d+)\*\*", text, re.IGNORECASE
    ) or re.search(r"horizon\s+(\d{3,4})\b", text, re.IGNORECASE)
    if not horizon_m:
        raise ValueError(f"pre-registration {prereg} has no parseable horizon.")
    horizon = int(horizon_m.group(1))

    cost_m = re.search(r"[≥>=]\s*([0-9]*\.?[0-9]+)\s*[×x]\s*cost", text, re.IGNORECASE)
    if not cost_m:
        raise ValueError(f"pre-registration {prereg} has no parseable ≥N× cost hurdle.")
    cost_law_multiple = float(cost_m.group(1))

    for key in tier_keys:
        if key not in FIRM_RULES:
            raise ValueError(f"frozen tier {key!r} not present in FIRM_RULES.")

    # Staleness guard. A pre-registration is deliberately immutable and is never
    # deleted when superseded (it is the audit record that a ceiling change was an
    # open, dated override rather than a quiet edit). That makes a superseded file
    # permanently parseable, so an explicit `path=` can silently return a DEAD gate.
    # WARN, never raise: reproducing a historical run against its own frozen ceiling
    # is a legitimate and necessary use (control arms, reproduction checks).
    # Anchor: 2026-09-02 — a retrieved harness hard-coded the v1 path and scored the
    # W1 bootstrap partition against 3.0% a week after the live ceiling became 5.0%.
    superseded_note = None
    status_m = re.search(r"^\*\*Status:\*\*\s*(.+)$", text, re.MULTILINE)
    if status_m:
        status_text = status_m.group(1).strip().strip("`").strip()
        if re.search(r"\b(CLOSED|SUPERSEDED)\b", status_text, re.IGNORECASE):
            superseded_note = status_text
            warnings.warn(
                f"scoring thresholds parsed from a SUPERSEDED pre-registration: "
                f"{prereg.name} — Status: {status_text}. "
                f"eval_bust_ceiling={eval_bust:.1f}% is a HISTORICAL number, not the "
                f"live gate (live default: {DEFAULT_PREREG.name}). Intentional only "
                f"for reproducing a historical run against its own frozen ceiling.",
                StaleGateWarning,
                stacklevel=2,
            )

    return ScoringThresholds(
        eval_bust_ceiling=eval_bust / 100.0,
        funded_bust_ceiling=funded_bust / 100.0,
        pass_floor=pass_floor / 100.0,
        tier_keys=tier_keys,
        seeds=seeds,
        sims_per_seed=sims_per_seed,
        horizon=horizon,
        cost_law_multiple=cost_law_multiple,
        source_path=str(prereg),
        superseded_note=superseded_note,
    )


def reduce_to_deployable(
    full_res_trades: Sequence[float],
    deployable_daily_pnl: np.ndarray,
    *,
    envelope_verdict: EnvelopeVerdict,
) -> G1Result:
    """G1 — record R_deploy + expectancy ratio; halt on envelope NO."""
    trades = [float(x) for x in full_res_trades]
    daily = np.asarray(deployable_daily_pnl, dtype=float).reshape(-1)
    r_deploy = len(trades)
    mean_trades = float(np.mean(trades)) if trades else float("nan")
    mean_daily = float(np.mean(daily)) if daily.size else float("nan")
    if mean_trades == 0.0 or not np.isfinite(mean_trades):
        ratio = float("nan")
    else:
        ratio = mean_daily / mean_trades
    halted = envelope_verdict == "NO"
    return G1Result(
        r_deploy=r_deploy,
        expectancy_ratio=ratio,
        deployable_default_envelope=envelope_verdict,
        halted=halted,
    )


def cost_law_kill(
    firm_key: str,
    *,
    r_deploy: int,
    gross_edge_usd: float,
    thresholds: ScoringThresholds,
) -> G2Result:
    """G2 — ≥N× round-trip cost hurdle at R_deploy using firm cost_per_side_usd."""
    if firm_key not in FIRM_RULES:
        raise KeyError(firm_key)
    cps = FIRM_RULES[firm_key].get("cost_per_side_usd")
    if cps is None:
        raise ValueError(f"{firm_key!r} has no cost_per_side_usd — G2 blocked.")
    cps_f = float(cps)
    rt = 2.0 * cps_f
    hurdle = thresholds.cost_law_multiple * rt * float(r_deploy)
    passed = float(gross_edge_usd) >= hurdle
    return G2Result(
        firm_key=firm_key,
        cost_per_side_usd=cps_f,
        rt_cost_usd=rt,
        hurdle_usd=hurdle,
        gross_edge_usd=float(gross_edge_usd),
        passed=passed,
    )


def blocks_from_daily_pnl(candidate_daily_pnl: np.ndarray) -> np.ndarray:
    """Build Mon-anchored 5-day week-blocks for ``run_seed`` from a 1-D daily series.

    Shape out: ``(n_weeks, 5, 1)`` — single-leg candidate attribution.
    """
    pnl = np.asarray(candidate_daily_pnl, dtype=float).reshape(-1)
    if pnl.size < 5:
        raise ValueError(
            f"candidate_daily_pnl needs ≥5 business days to form a week-block; got {pnl.size}"
        )
    # 2020-01-06 is a Monday — matches build_week_blocks Mon-anchor rule.
    idx = pd.bdate_range("2020-01-06", periods=pnl.size)
    panel = pd.DataFrame({"candidate": pnl}, index=idx)
    blocks = build_week_blocks(panel)
    if len(blocks) == 0:
        raise ValueError("build_week_blocks returned 0 blocks — check calendar alignment.")
    return blocks


def paired_blocks_from_daily(
    daily_pnl: np.ndarray,
    intraday_low: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Build paired Mon-anchored week-blocks for P&L and ``intraday_low``.

    Both channels share the same ``pd.bdate_range("2020-01-06", …)`` index so
    week-anchoring cannot drift. Shape out: ``(n_weeks, 5, 1)`` each.

    INVARIANT (frozen Phase-4 §1): the intraday channel is never re-derived or
    re-drawn independently of the P&L channel.

    Invalid input (length mismatch, <5 days, any ``low > 0``, or a non-finite
    value in EITHER channel) raises ``ValueError``. NaN/±inf are rejected
    explicitly because ``NaN > 0`` compares False, so the sign check cannot see
    them (O-4 Slice A §2.1).
    """
    pnl = np.asarray(daily_pnl, dtype=float).reshape(-1)
    low = np.asarray(intraday_low, dtype=float).reshape(-1)
    if pnl.size != low.size:
        raise ValueError(
            f"daily_pnl length {pnl.size} != intraday_low length {low.size}"
        )
    if pnl.size < 5:
        raise ValueError(
            f"paired daily series need ≥5 business days; got {pnl.size}"
        )
    if np.any(low > 0.0):
        raise ValueError(
            "intraday_low entries must be ≤ 0.0 (excursion from day's opening equity)"
        )
    if not np.isfinite(pnl).all() or not np.isfinite(low).all():
        raise ValueError(
            "daily_pnl and intraday_low must both be finite "
            "(NaN or ±inf rejected in either channel)"
        )
    idx = pd.bdate_range("2020-01-06", periods=pnl.size)
    panel = pd.DataFrame({"candidate": pnl, "intraday_low": low}, index=idx)
    values = panel.to_numpy(dtype=float)
    blocks = np.array(
        [
            values[i : i + 5]
            for i, day in enumerate(panel.index)
            if day.weekday() == 0 and i + 5 <= len(panel)
        ]
    )
    if len(blocks) == 0:
        raise ValueError("paired week-blocks empty — check calendar alignment.")
    # (n_weeks, 5, 1) keeps the single-leg strategy axis simulate_path sums over.
    return blocks[:, :, 0:1].copy(), blocks[:, :, 1:2].copy()


def make_alt_panel_paired(
    daily_pnl: np.ndarray,
    intraday_low: np.ndarray,
    *,
    target_len: int,
    block_size: int,
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray]:
    """Contiguous-block bootstrap with one RNG draw applied to both channels.

    INVARIANT (frozen Phase-4 §1 resample #1): ``st`` is drawn once; both arrays
    are sliced at the same ``st : st + block_size`` offsets.
    """
    pnl = np.asarray(daily_pnl, dtype=float).reshape(-1)
    low = np.asarray(intraday_low, dtype=float).reshape(-1)
    if pnl.size != low.size:
        raise ValueError(
            f"daily_pnl length {pnl.size} != intraday_low length {low.size}"
        )
    n_avail = target_len - block_size + 1
    if n_avail < 1:
        raise ValueError(
            f"panel too short for block bootstrap: len={target_len} block={block_size}"
        )
    sampled_p: list[np.ndarray] = []
    sampled_l: list[np.ndarray] = []
    tot = 0
    while tot < target_len:
        st = int(rng.integers(0, n_avail))
        sampled_p.append(pnl[st : st + block_size])
        sampled_l.append(low[st : st + block_size])
        tot += block_size
    return (
        np.concatenate(sampled_p)[:target_len],
        np.concatenate(sampled_l)[:target_len],
    )


def assert_intraday_channel_nonvacuous(
    blocks: np.ndarray,
    intraday_blocks: np.ndarray,
    *,
    thresholds: ScoringThresholds,
    firm_key: str,
    n_sims: int,
    firm_kwargs_override: dict | None = None,
    horizon: int | None = None,
    protected_blocks: np.ndarray | None = None,
    protected_intraday_blocks: np.ndarray | None = None,
    mode_trigger: float | None = None,
    capture: dict | None = None,
) -> dict:
    """Mandatory non-vacuity guard (frozen Phase-4 §1).

    ``capture`` (OPTIONAL, size-feasibility prereg §2.3 item 2) receives each arm's
    summary under ``"eod"``, ``"zeros"`` and ``"real"`` as it is computed, before the
    assertions, so it is complete even when the guard raises. ``None`` is a no-op.

    Zeros-channel must reproduce close-only figures byte-for-byte; the real
    channel must differ. A silently dropped ``intraday_low`` would reproduce the
    flattering EOD numbers — the M-23-shaped failure mode.

    ``protected_blocks`` / ``protected_intraday_blocks`` / ``mode_trigger``
    (OPTIONAL) — the mode-switching channel (card 2026-10-05 §0.5 item 5). Given,
    EVERY arm runs with them (the EOD arm included), so the guard still compares
    like-for-like channels; the zeros arm zeros BOTH intraday channels and the
    real arm uses both. Absent, the guard is byte-identical to the legacy call.
    """
    horiz = thresholds.horizon if horizon is None else int(horizon)
    kw = (
        dict(firm_kwargs_override)
        if firm_kwargs_override is not None
        else firm_kwargs(firm_key, inactivity_off=True, consistency=_consistency_frac(firm_key))
    )
    # Fail closed (Codex 4190226566): the guard always has an intraday channel, so a
    # requested mode switch needs all three protected inputs. None is ever dropped.
    mode_given = [
        name
        for name, value in (
            ("protected_blocks", protected_blocks),
            ("protected_intraday_blocks", protected_intraday_blocks),
            ("mode_trigger", mode_trigger),
        )
        if value is not None
    ]
    if mode_given and len(mode_given) != 3:
        raise ValueError(
            "incomplete mode-switching inputs for the guard: got "
            f"{mode_given}; protected_blocks, protected_intraday_blocks and "
            "mode_trigger are given together or not at all"
        )
    zeros = np.zeros_like(intraday_blocks)
    protected_zeros = np.zeros_like(intraday_blocks) if protected_blocks is not None else None

    def _score(intra: np.ndarray | None, protected_intra: np.ndarray | None = None) -> dict:
        mode_kwargs: dict = {}
        if protected_blocks is not None:
            mode_kwargs["protected_blocks"] = protected_blocks
            mode_kwargs["mode_trigger"] = mode_trigger
        if protected_intra is not None:
            mode_kwargs["protected_intraday_blocks"] = protected_intra
        seeds_results = [
            run_seed(
                seed,
                int(n_sims),
                blocks,
                NO_PROTECTION_TRIGGER,
                DD_SCALE,
                horizon=horiz,
                strats=CANDIDATE_STRAT,
                firm_kwargs=kw,
                intraday_blocks=intra,
                **mode_kwargs,
            )
            for seed in thresholds.seeds
        ]
        return summarize_outcomes(seeds_results, int(n_sims))

    sink = capture if capture is not None else {}
    eod = sink["eod"] = _score(None)
    zero_arm = sink["zeros"] = _score(zeros, protected_zeros)
    real_arm = sink["real"] = _score(intraday_blocks, protected_intraday_blocks)

    if (
        float(zero_arm["headline_bust"]) != float(eod["headline_bust"])
        or float(zero_arm["pass_rate"]) != float(eod["pass_rate"])
    ):
        raise AssertionError(
            "non-vacuity FAIL: zeros-channel must reproduce EOD (close-only) "
            f"byte-for-byte; eod bust={eod['headline_bust']} pass={eod['pass_rate']} "
            f"vs zeros bust={zero_arm['headline_bust']} pass={zero_arm['pass_rate']}"
        )
    if (
        float(real_arm["headline_bust"]) == float(eod["headline_bust"])
        and float(real_arm["pass_rate"]) == float(eod["pass_rate"])
    ):
        raise AssertionError(
            "non-vacuity FAIL: real intraday_low channel is vacuous — figures "
            "identical to EOD (channel silently dropped or all-zero). "
            f"bust={eod['headline_bust']} pass={eod['pass_rate']}"
        )
    return {"eod": eod, "zeros": zero_arm, "real": real_arm}


def _f2_label(firm_key: str) -> str | None:
    dd = FIRM_RULES[firm_key].get("dd_type")
    if dd == "trailing":
        return "optimistic-lower-bound"
    return None


def _consistency_frac(firm_key: str) -> float | None:
    raw = FIRM_RULES[firm_key].get("consistency_rule_pct")
    if raw is None:
        return None
    return float(raw) / 100.0


def run_tier_remc(
    firm_key: str,
    blocks: np.ndarray,
    thresholds: ScoringThresholds,
    *,
    n_sims: int | None = None,
    consistency: float | None = None,
    intraday_blocks: np.ndarray | None = None,
    protected_blocks: np.ndarray | None = None,
    protected_intraday_blocks: np.ndarray | None = None,
    mode_trigger: float | None = None,
    capture: dict | None = None,
) -> dict:
    """G4 — one run_seed loop for one (tier, consistency) setting via firm_kwargs.

    ``capture`` (OPTIONAL, size-feasibility prereg §2.3 item 3) receives the pooled
    ``days_to_pass`` of every passing sim across seeds and the pooled sim count
    ``n``. ``None`` is a no-op; the return value is unchanged either way.

    ``intraday_blocks`` — optional paired week-blocks of per-day equity excursions
    (same indices as ``blocks``). Threaded into ``run_seed`` → ``simulate_path``.

    ``protected_blocks`` / ``protected_intraday_blocks`` / ``mode_trigger``
    (OPTIONAL) — the mode-switching channel (card 2026-10-05 §0.5 item 4),
    threaded into ``run_seed`` only when given, so the default call is
    byte-identical. The trigger value is the caller's (the operator-ruling
    book threshold), never a value chosen here.
    """
    assert_engine_ready(firm_key)  # G3 gate; raises on failure
    sims = thresholds.sims_per_seed if n_sims is None else int(n_sims)
    kw = firm_kwargs(firm_key, inactivity_off=True, consistency=consistency)
    mode_kwargs: dict = {}
    if protected_blocks is not None:
        mode_kwargs["protected_blocks"] = protected_blocks
    if protected_intraday_blocks is not None:
        mode_kwargs["protected_intraday_blocks"] = protected_intraday_blocks
    if mode_trigger is not None:
        mode_kwargs["mode_trigger"] = mode_trigger
    seeds_results = [
        run_seed(
            seed,
            sims,
            blocks,
            NO_PROTECTION_TRIGGER,
            DD_SCALE,
            horizon=thresholds.horizon,
            strats=CANDIDATE_STRAT,
            firm_kwargs=kw,
            intraday_blocks=intraday_blocks,
            **mode_kwargs,
        )
        for seed in thresholds.seeds
    ]
    summary = summarize_outcomes(seeds_results, sims)
    if capture is not None:
        capture["days_to_pass"] = [int(d) for r in seeds_results for d in r["days_to_pass"]]
        capture["n"] = sims * len(seeds_results)
    return {
        "firm_key": firm_key,
        "consistency": consistency,
        "n_sims": sims,
        "seeds": list(thresholds.seeds),
        "summary": summary,
        "headline_bust": summary["headline_bust"],
        "pass_rate": summary["pass_rate"],
        "intraday_low": intraday_blocks is not None,
    }


def score_part_a(
    run_summary: dict,
    thresholds: ScoringThresholds,
) -> bool:
    """Part A: headline bust ≤ ceiling AND pass ≥ floor (Run-2)."""
    return (
        float(run_summary["headline_bust"]) <= thresholds.eval_bust_ceiling
        and float(run_summary["pass_rate"]) >= thresholds.pass_floor
    )


def score_funded(
    run_summary: dict,
    thresholds: ScoringThresholds,
) -> bool:
    """Part B diagnostic — funded ruin ceiling; does NOT gate §4."""
    return float(run_summary["headline_bust"]) <= thresholds.funded_bust_ceiling


def discharges_falsifier(
    tier_scores: dict[str, TierScore],
    thresholds: ScoringThresholds,
) -> bool:
    """G8 — ≥2 distinct firms clear Part A, of which ≥1 is trailing_locking."""
    clearers = [k for k, s in tier_scores.items() if s.clears_part_a]
    if len(clearers) < 2:
        return False
    locking = thresholds.trailing_locking_tiers
    return any(k in locking for k in clearers)


def score_candidate(
    *,
    strategy_label: str,
    candidate_daily_pnl: np.ndarray,
    full_res_trades: Sequence[float],
    envelope_verdict: EnvelopeVerdict,
    thresholds: ScoringThresholds | None = None,
    n_sims: int | None = None,
    gross_edge_usd: float | None = None,
    tiers: Sequence[str] | None = None,
    intraday_low: np.ndarray | None = None,
    tier_series: Mapping[str, TierSeries] | None = None,
    mode_trigger: float | None = None,
    sidecar: dict | None = None,
) -> ScoringReport:
    """Run G0–G8 for one candidate across the frozen (or overridden) tier set.

    ``n_sims`` defaults to the pre-reg 10k; tests pass a smaller value for speed.
    ``tiers`` defaults to the frozen four; override only in unit tests that isolate
    a geometry (never for a live scoring claim).

    ``intraday_low`` — optional per-day equity-excursion series (≤ 0, same length
    as ``candidate_daily_pnl``; O-4 Slice A). Given, it is paired into week-blocks
    BEFORE G1 (invalid input raises even when G1 would halt) and threaded into
    every G4 run on every tier that reaches G4, so each tier read tests the
    barrier against the intraday excursion (the mandatory intraday-honest clock,
    operator ruling 2026-10-02 / prereg I-12). The frozen non-vacuity guard runs
    once per gating tier at the gating depth; a vacuous tier records a reason and
    the report is labelled ``gate_grade=False`` (INSUFFICIENT), never silently
    gate-grade. ``None`` keeps the legacy EOD-clock path byte-identical, which is
    reportable and never gates a clear.

    ``tier_series`` — optional per-tier series (prereg I-19, step 2(c)): each tier
    runs G4 and its guard on its own cost-netted series and excursion, in one call
    and one report. It must hold exactly the scored tiers (fail closed); it
    excludes the single ``intraday_low`` argument. ``candidate_daily_pnl`` still
    feeds G1. ``mode_trigger`` with each tier's protected channels enables I-17
    mode-switching once the kernel supports it; otherwise the call raises.

    ``sidecar`` (OPTIONAL, size-feasibility prereg §2.3 items 2-4) is filled per tier
    that reaches G4 with ``guard_arms`` (the guard's three arms, captured before its
    assertions), ``gate_grade_reasons`` (that tier's reason text verbatim) and
    ``days_to_pass`` (``run1``/``run2`` pooled captures). ``None`` passes nothing new
    to the guard or G4, so the default call and report are byte-identical.
    """
    thr = thresholds if thresholds is not None else load_scoring_thresholds()
    tier_keys = tuple(tiers) if tiers is not None else thr.tier_keys
    # Guard depth is the gating depth (card §0.5(A)); no new depth parameter (O-6).
    sims = n_sims if n_sims is not None else thr.sims_per_seed

    # Pair + validate the channel BEFORE G1 so an invalid channel raises even
    # when G1 would halt. The returned P&L blocks share the Monday-anchor rule
    # with blocks_from_daily_pnl, so the tier reads are index-identical.
    intraday_blocks: np.ndarray | None = None
    per_tier: dict[str, dict] | None = None
    if tier_series is not None:
        if intraday_low is not None:
            raise ValueError("tier_series carries each tier's intraday_low; do not also pass intraday_low")
        per_tier, honest = _tier_blocks(tier_series, tier_keys, mode_trigger)
    elif mode_trigger is not None:
        raise ValueError("mode_trigger requires tier_series with protected channels")
    if intraday_low is not None:
        blocks, intraday_blocks = paired_blocks_from_daily(
            candidate_daily_pnl, intraday_low
        )
    channel_given = intraday_low is not None or (per_tier is not None and honest)

    g1 = reduce_to_deployable(
        full_res_trades,
        candidate_daily_pnl,
        envelope_verdict=envelope_verdict,
    )
    report = ScoringReport(
        strategy_label=strategy_label,
        g1=g1,
        thresholds_source=thr.source_path,
    )
    gate_reasons: list[str] = []
    if not channel_given:
        report.breach_clock = "eod"
        report.gate_grade_reasons = [
            "no intraday_low supplied: EOD-clock read is reportable, never gating (prereg I-12)"
        ]
    else:
        report.breach_clock = "intraday_honest"
        report.gate_grade_reasons = gate_reasons
    if g1.halted:
        report.halted_at = "G1"
        # No tier reached G4, so no breach-clock read exists to fail (§0.5(C)).
        report.gate_grade = channel_given and not gate_reasons
        return report

    edge = (
        float(gross_edge_usd)
        if gross_edge_usd is not None
        else float(np.sum(full_res_trades))
    )
    if intraday_blocks is None and per_tier is None:
        blocks = blocks_from_daily_pnl(candidate_daily_pnl)

    for firm_key in tier_keys:
        g2 = cost_law_kill(
            firm_key,
            r_deploy=g1.r_deploy,
            gross_edge_usd=edge,
            thresholds=thr,
        )
        report.g2_by_tier[firm_key] = g2
        if not g2.passed:
            # Cost-law kill stops this tier; continue others (per-firm cost schedules).
            report.tiers[firm_key] = TierScore(
                firm_key=firm_key,
                dd_type=str(FIRM_RULES[firm_key].get("dd_type")),
                f2_label=_f2_label(firm_key),
                g3_ok=False,
                run1={},
                run2={},
                clears_part_a=False,
                clears_funded=False,
                gated_on="g2_killed",
            )
            continue

        # G3
        assert_engine_ready(firm_key)

        mode_kwargs: dict = {}
        if per_tier is not None:
            tier = per_tier[firm_key]
            blocks, intraday_blocks = tier["blocks"], tier["intraday_blocks"]
            mode_kwargs = {k: tier[k] for k in ("protected_blocks", "protected_intraday_blocks",
                                                "mode_trigger") if k in tier}

        # Opt-in capture: only when a sidecar is requested is anything new passed on.
        cap = None
        if sidecar is not None:
            cap = sidecar[firm_key] = {"guard_arms": {}, "gate_grade_reasons": [], "days_to_pass": {}}

        # Mandatory non-vacuity guard (frozen Phase-4 §1) at the gating depth.
        # Only a "non-vacuity FAIL" AssertionError is a vacuity finding — any
        # other AssertionError (e.g. the summarize_outcomes bucket-sum
        # invariant) is an engine fault and must propagate.
        if intraday_blocks is not None:
            try:
                assert_intraday_channel_nonvacuous(
                    blocks,
                    intraday_blocks,
                    thresholds=thr,
                    firm_key=firm_key,
                    n_sims=sims,
                    **mode_kwargs,
                    **({} if cap is None else {"capture": cap["guard_arms"]}),
                )
            except AssertionError as exc:
                if not str(exc).startswith("non-vacuity FAIL"):
                    raise
                gate_reasons.append(f"{firm_key}: non-vacuity failed: {exc}")
                if cap is not None:
                    cap["gate_grade_reasons"].append(gate_reasons[-1])

        # G4 Run-1 (consistency off) + Run-2 (consistency on where present).
        # The honest clock runs regardless of the guard outcome: figures stay
        # reportable even when the channel is vacuous. intraday_blocks stays
        # off the kwargs entirely on the EOD path (byte-identical call).
        remc_kwargs: dict = dict(mode_kwargs)
        if intraday_blocks is not None:
            remc_kwargs["intraday_blocks"] = intraday_blocks

        def _dtp(run: str) -> dict:
            return {} if cap is None else {"capture": cap["days_to_pass"].setdefault(run, {})}

        run1 = run_tier_remc(
            firm_key, blocks, thr, n_sims=n_sims, consistency=None, **remc_kwargs, **_dtp("run1")
        )
        cons = _consistency_frac(firm_key)
        if cons is None:
            run2 = run1
            gated_on = "run1_degenerate"
            if cap is not None:
                cap["days_to_pass"]["run2"] = cap["days_to_pass"]["run1"]
        else:
            run2 = run_tier_remc(
                firm_key, blocks, thr, n_sims=n_sims, consistency=cons, **remc_kwargs, **_dtp("run2")
            )
            gated_on = "run2"

        clears_a = score_part_a(run2, thr)
        clears_f = score_funded(run2, thr)
        report.tiers[firm_key] = TierScore(
            firm_key=firm_key,
            dd_type=str(FIRM_RULES[firm_key].get("dd_type")),
            f2_label=_f2_label(firm_key),
            g3_ok=True,
            run1={
                "headline_bust": run1["headline_bust"],
                "pass_rate": run1["pass_rate"],
                "rates": run1["summary"]["rates"],
            },
            run2={
                "headline_bust": run2["headline_bust"],
                "pass_rate": run2["pass_rate"],
                "rates": run2["summary"]["rates"],
            },
            clears_part_a=clears_a,
            clears_funded=clears_f,
            gated_on=gated_on,
        )

    # G6 — single candidate → STANDALONE (pre-reg note)
    report.routing = "STANDALONE"
    # G7 — diagnostic only
    report.funded_ruin_tier_count = sum(
        1 for s in report.tiers.values() if s.clears_funded
    )
    # G8
    report.discharges_falsifier = discharges_falsifier(report.tiers, thr)
    # Gate grade is report-level (one vacuous tier ⇒ the whole read is
    # INSUFFICIENT); it is reported beside — never combined with — the
    # discharge. A gate-grade discharge reads both (I-12).
    report.gate_grade = channel_given and not gate_reasons
    return report


def naive_daily_static_bust(summary_rates: dict) -> float:
    """F1 trap shape — daily+static only (what compute_default_config reports)."""
    return float(summary_rates["bust_daily"]) + float(summary_rates["bust_static"])


__all__ = [
    "CANDIDATE_STRAT",
    "DD_SCALE",
    "DEFAULT_PREREG",
    "NO_PROTECTION_TRIGGER",
    "G1Result",
    "G2Result",
    "ScoringReport",
    "ScoringThresholds",
    "TierScore",
    "TierSeries",
    "assert_intraday_channel_nonvacuous",
    "blocks_from_daily_pnl",
    "cost_law_kill",
    "discharges_falsifier",
    "load_scoring_thresholds",
    "make_alt_panel_paired",
    "naive_daily_static_bust",
    "paired_blocks_from_daily",
    "reduce_to_deployable",
    "run_tier_remc",
    "score_candidate",
    "score_funded",
    "score_part_a",
]


def main(argv: Sequence[str] | None = None) -> int:
    """Thin CLI — score a candidate daily-P&L CSV against the frozen four tiers."""
    import argparse
    import sys

    ap = argparse.ArgumentParser(
        description=(
            "Prop survivor-scoring harness (G0–G8). Reads a one-column daily P&L "
            "CSV and the frozen pre-registration; writes a JSON report. Does not "
            "switch ACTIVE_FIRM or edit firm rules."
        )
    )
    ap.add_argument("--label", required=True, help="strategy_label for the report")
    ap.add_argument(
        "--daily-pnl-csv",
        required=True,
        help="CSV with a single numeric column (or named 'pnl'/'candidate')",
    )
    ap.add_argument(
        "--trades-csv",
        required=True,
        help="CSV with a single numeric column of full-resolution trade P&Ls (G1 R_deploy)",
    )
    ap.add_argument(
        "--envelope",
        choices=("YES", "NO"),
        required=True,
        help="DEPLOYABLE-DEFAULT-ENVELOPE verdict from the producing brief",
    )
    ap.add_argument("--out", required=True, help="output JSON path")
    ap.add_argument("--prereg", default=str(DEFAULT_PREREG), help="pre-registration path")
    ap.add_argument(
        "--n-sims",
        type=int,
        default=None,
        help="override sims/seed (default: pre-reg 10k; use smaller for smoke tests)",
    )
    ap.add_argument(
        "--intraday-low-csv",
        default=None,
        help=(
            "CSV of per-day intraday equity excursions (column 'intraday_low' or "
            "the first column); row count must match --daily-pnl-csv, else "
            "paired_blocks_from_daily raises"
        ),
    )
    args = ap.parse_args(list(argv) if argv is not None else None)

    daily_df = pd.read_csv(args.daily_pnl_csv)
    trades_df = pd.read_csv(args.trades_csv)

    def _col(df: pd.DataFrame) -> np.ndarray:
        for name in ("pnl", "candidate", "daily_pnl", "net"):
            if name in df.columns:
                return df[name].to_numpy(dtype=float)
        return df.iloc[:, 0].to_numpy(dtype=float)

    intraday_low_arg: np.ndarray | None = None
    if args.intraday_low_csv is not None:
        low_df = pd.read_csv(args.intraday_low_csv)
        if "intraday_low" in low_df.columns:
            intraday_low_arg = low_df["intraday_low"].to_numpy(dtype=float)
        else:
            intraday_low_arg = low_df.iloc[:, 0].to_numpy(dtype=float)

    thr = load_scoring_thresholds(args.prereg)
    report = score_candidate(
        strategy_label=args.label,
        candidate_daily_pnl=_col(daily_df),
        full_res_trades=list(_col(trades_df)),
        envelope_verdict=args.envelope,  # type: ignore[arg-type]
        thresholds=thr,
        n_sims=args.n_sims,
        intraday_low=intraday_low_arg,
    )
    report.write_json(args.out)
    print(
        f"[prop-survivor-scoring] label={args.label} "
        f"discharges_falsifier={report.discharges_falsifier} "
        f"halted_at={report.halted_at} "
        f"breach_clock={report.breach_clock} gate_grade={report.gate_grade} "
        f"-> {args.out}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
