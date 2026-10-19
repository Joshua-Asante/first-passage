"""Hash-bound solo export adapter; no strategy replay, scorer or MC entry point.

Envelope provenance: 2026-10-05 four-firm series-builder card §0.5(5–6).
For each day: low = -sum(abs(trade MAE)) - full tier day costs.
This bounds modeled losses conditional on complete, same-day lot records and
valid per-lot MAE. It is not a synchronized path or an intraday peak ratchet.
Only synthetic series are generated before this study's ratified freeze.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation
import hashlib
import json
import math
from pathlib import Path
import re
from typing import Sequence

import numpy as np

from firm_rules import FIRM_RULES
from discovery.remc_series_builder import (
    CME_REOPEN_ET, LATE_EXIT_ET, NY_TZ, Trade, TradeListError,
    assert_out_dir_allowed, cme_trade_date, load_trade_table, verify_sha256,
)

LEG = 'orb_mnq_v7'
STUDY_ROOT = Path('.cache/orb-mnq-v7-s4-2026-10')


@dataclass
class SoloSeries:
    dates: tuple[date, ...]
    tiers: dict[str, dict[str, np.ndarray]]
    manifest: dict


def _validate_trades(trades: Sequence[Trade], expected_quantity: int) -> None:
    if type(expected_quantity) is not int or expected_quantity <= 0:
        raise ValueError('expected quantity must be a positive integer')
    if not trades:
        raise ValueError('empty trade list')
    seen = set()
    for t in trades:
        if t.leg != LEG:
            raise ValueError('foreign leg in solo input')
        if t.trade_number in seen:
            raise ValueError('duplicate trade number')
        seen.add(t.trade_number)
        if not all(math.isfinite(v) for v in (t.qty, t.net_usd, t.commission_usd, t.adverse_excursion_usd)):
            raise ValueError('trade values must be finite')
        if t.qty != expected_quantity:
            raise ValueError('quantity differs from the elected as-captured lot size; no rescaling')
        if t.commission_usd < 0:
            raise ValueError('negative commission')
        if t.entry_ny.utcoffset() is None or t.exit_ny.utcoffset() is None:
            raise ValueError('timezone-aware timestamps required')
        entry = t.entry_ny.astimezone(NY_TZ)
        exit_ = t.exit_ny.astimezone(NY_TZ)
        if exit_ < entry:
            raise ValueError('invalid entry/exit chronology')
        if entry.date() != exit_.date():
            raise ValueError('solo lots must enter/exit on the same NY civil day')
        if cme_trade_date(entry) != cme_trade_date(exit_):
            raise ValueError('different CME trade dates')
        if LATE_EXIT_ET <= exit_.time() < CME_REOPEN_ET:
            raise ValueError('exit at/after source session close')
        if exit_.weekday() >= 5:
            raise ValueError('weekend lot is not a weekday session')
        # Compare reported decimal amounts, without a tolerance that could waive
        # a small uncovered loss or binary addition inventing a discrepancy.
        gross_decimal = Decimal(str(t.net_usd)) + Decimal(str(t.commission_usd))
        if abs(Decimal(str(t.adverse_excursion_usd))) < max(Decimal(0), -gross_decimal):
            raise ValueError('MAE does not cover realized gross loss; refuse, never repair it')


def load_solo_export(path: str | Path, expected_sha256: str, *, export_tz: str,
                     expected_quantity: int, capture_commission_per_side: float) -> list[Trade]:
    """Hash before parse, reuse strict pairing, validate elected lots, hash again.

    Partial quantity rows and ambiguous split/duplicate trade numbers are refused.
    This consumes exported lots, never synthesizes fills from strategy code.
    """
    if not math.isfinite(capture_commission_per_side) or capture_commission_per_side < 0:
        raise ValueError('invalid capture commission')
    trades = load_trade_table(path, expected_sha256, leg=LEG, export_tz=export_tz)
    with Path(path).open(encoding='utf-8-sig', newline='') as handle:
        rows = list(csv.DictReader(handle))
    kinds = {row['Type'].strip().lower() for row in rows}
    if kinds != {'entry long', 'exit long'}:
        raise TradeListError('elected capture requires paired long-only rows')
    # The shared parser intentionally falls back to Entry cells and otherwise
    # prefers Exit. That projection alone cannot prove a complete fixed lot.
    for row in rows:
        raw_quantity = (row.get('Size (qty)') or '').strip()
        if not raw_quantity:
            raise ValueError('quantity must be present on both raw paired rows')
        try:
            quantity = Decimal(raw_quantity)
        except InvalidOperation as exc:
            raise ValueError('invalid raw paired-row quantity') from exc
        if not quantity.is_finite() or quantity != expected_quantity:
            raise ValueError('both raw rows must establish the elected complete quantity')
    _validate_trades(trades, expected_quantity)
    for t in trades:
        if not math.isclose(t.commission_usd, 2*t.qty*capture_commission_per_side, abs_tol=1e-8):
            raise ValueError('commission differs from elected capture settings')
    verify_sha256(path, expected_sha256)
    return trades


def complete_week_window(trades: Sequence[Trade]) -> tuple[date, date]:
    """Keep only full real Mon–Fri weeks inside observed trade-date bounds.

    No invented zero days outside the observed bounds; both boundary exclusions
    are disclosed. This result-independent policy must be ratified before use.
    """
    first = min(t.entry_ny.astimezone(NY_TZ).date() for t in trades)
    last = max(t.exit_ny.astimezone(NY_TZ).date() for t in trades)
    start = first + timedelta(days=(-first.weekday()) % 7)
    end = last - timedelta(days=(last.weekday()-4) % 7)
    if start > end:
        raise ValueError('observed bounds contain no complete week')
    return start, end


def build_solo_series(trades: Sequence[Trade], *, expected_quantity: int,
                      tier_keys: Sequence[str]) -> SoloSeries:
    """Pure producer. Explicit tier keys; normal/as-exported, protection OFF.

    Costs come from canonical firm rows. This performs no engine preflight,
    cost-law kill, tier acceptance, pass/bust calculation or gate assignment.
    """
    _validate_trades(trades, expected_quantity)
    tiers = tuple(tier_keys)
    if not tiers or len(set(tiers)) != len(tiers):
        raise ValueError('missing or duplicate tier keys')
    costs = {}
    for key in tiers:
        if key not in FIRM_RULES:
            raise ValueError(f'unknown tier {key}')
        rule = FIRM_RULES[key]
        cost = rule.get('cost_per_side_usd')
        if (not isinstance(cost, (int, float)) or isinstance(cost, bool) or
                not math.isfinite(cost) or cost < 0):
            raise ValueError(f'unadmitted cost/rule context for tier {key}')
        costs[key] = float(cost)
    start, end = complete_week_window(trades)
    dates = tuple(start + timedelta(days=i) for i in range((end-start).days+1)
                  if (start+timedelta(days=i)).weekday() < 5)
    groups = {d: [] for d in dates}
    excluded = []
    for t in trades:
        day = t.exit_ny.astimezone(NY_TZ).date()
        if day in groups:
            groups[day].append(t)
        else:
            excluded.append(t.trade_number)
    gross = np.array([math.fsum(t.gross_usd for t in groups[d]) for d in dates])
    sides = np.array([math.fsum(2*t.qty for t in groups[d]) for d in dates])
    adverse = np.array([math.fsum(abs(t.adverse_excursion_usd) for t in groups[d]) for d in dates])
    channels = {}
    for key, cost in costs.items():
        fee = sides*cost
        pnl = gross-fee
        low = 0.-adverse-fee
        if not np.isfinite(pnl).all() or not np.isfinite(low).all():
            raise ValueError('daily series overflow/nonfinite value')
        channels[key] = {'pnl': pnl, 'low': low}
    manifest = {
        'schema': 'orb-solo-series/v1', 'scored': False,
        'clock_kind': 'conservative_mae_envelope', 'mode': 'NORMAL', 'protection': 'OFF',
        'quantity_policy': 'as_captured', 'window_policy': 'complete_real_weeks_inside_observed_bounds',
        'window_start': start.isoformat(), 'window_end': end.isoformat(),
        'timezone': 'America/New_York', 'session_basis': 'same_NY_civil_day_and_CME_trade_date',
        'boundary_excluded_trade_numbers': sorted(excluded), 'cost_per_side_usd': costs,
        'mae_assumption': 'complete per-lot MAE bounds every open loss and realized gross loss',
        'limitations': ['not synchronized intraday equity', 'no intraday peak ratchet',
                        'no venue/tier admission established', 'full-day costs charged in low'],
    }
    return SoloSeries(dates, channels, manifest)


def write_solo_bundle(bundle: SoloSeries, out_dir: str | Path, *, repo_root: str | Path,
                      input_sha256: str, configuration_sha256: str) -> Path:
    """New private output directory only; manifest last, each CSV hash-bound.

    The later frozen executor owns invoking this on real data and binding the
    engine/scorer/depth evidence. This writer does not grant that release.
    """
    for pin in (input_sha256, configuration_sha256):
        if not isinstance(pin, str) or re.fullmatch('[0-9a-f]{64}', pin) is None:
            raise ValueError('input/configuration digest must be lowercase SHA-256')
    root = Path(repo_root).resolve()
    custody = (root/STUDY_ROOT).resolve()
    # Check the resolved custody root itself: a symlink cannot broaden custody.
    if custody != root/STUDY_ROOT:
        raise ValueError('custody root resolves outside its designated lexical path')
    out = Path(out_dir).resolve()
    if out != custody and custody not in out.parents:
        raise ValueError('output outside study custody root')
    assert_out_dir_allowed(out, repo_root=root)
    out.mkdir(parents=True, exist_ok=False)
    files = {}
    for key, channels in bundle.tiers.items():
        if re.fullmatch('[A-Za-z0-9_]+', key) is None:
            raise ValueError('unsafe tier filename')
        path = out/f'{key}.csv'
        with path.open('w', newline='', encoding='utf-8') as handle:
            writer = csv.writer(handle)
            writer.writerow(('date', 'daily_pnl', 'intraday_low'))
            writer.writerows((d.isoformat(), repr(float(pnl)), repr(float(low)))
                             for d, pnl, low in zip(bundle.dates, channels['pnl'], channels['low'], strict=True))
        files[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    manifest = dict(bundle.manifest, input_sha256=input_sha256,
                    configuration_sha256=configuration_sha256, series_files=files)
    path = out/'manifest.json'
    path.write_text(json.dumps(manifest, indent=2, allow_nan=False), encoding='utf-8')
    return path
