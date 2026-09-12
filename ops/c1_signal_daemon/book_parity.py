"""Parity harness: replay a private adapter on a frozen CME panel, compare with the
captured TradingView export (Track B TB-A1..A4 acceptance).

Inputs (all private, located by environment variable or repo default):
* panel  — ``core/data/bar_data/<SYMBOL>_M15.csv`` (``FP_BAR_DATA_DIR`` overrides the dir)
* export — the captured TradingView List-of-Trades CSV named in
  ``lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/phase1_config.json``
  (``FP_TV_EXPORT_DIR`` overrides the search dir; located by filename, then
  verified by sha256 against the config)

The comparison key is (entry bar, exit bar) in the chart's display clock
(America/New_York), with quantity and fill prices compared per matched pair.
Tracked outputs are counts and first divergences only — never trade rows.
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from c1_signal_daemon.feed import Bar
from c1_signal_daemon.tv_broker_emulator import ClosedTrade, TVBrokerEmulator

_REPO_ROOT = Path(__file__).resolve().parents[2]
ET = ZoneInfo("America/New_York")
UTC = ZoneInfo("UTC")
PHASE1_CONFIG = (_REPO_ROOT / "lab" / "analysis" / "c1"
                 / "tradeify_seven_strategy_phase1_2026-09" / "phase1_config.json")

STRATEGY_ID_BY_LEG = {
    "aegis_6j": "aegis_6j1",
    "dj30_mym_p250": "striker_dj30_mym_pyramid_250",
    "vanguard_mgc": "vanguard_mgc_v04",
    "orb_mnq_v7": "orb_mnq_recon_v7",
}


def bar_data_dir() -> Path:
    override = os.environ.get("FP_BAR_DATA_DIR")
    return Path(override) if override else _REPO_ROOT / "core" / "data" / "bar_data"


def export_dir() -> Path:
    override = os.environ.get("FP_TV_EXPORT_DIR")
    return Path(override) if override else _REPO_ROOT / "core" / "data" / "tv_exports" / "cme"


def phase1_source(leg_id: str) -> dict:
    cfg = json.loads(PHASE1_CONFIG.read_text(encoding="utf-8"))
    sid = STRATEGY_ID_BY_LEG[leg_id]
    for s in cfg["strategies"]:
        if s["strategy_id"] == sid:
            return s
    raise KeyError(sid)


def load_panel(symbol: str, *, start: datetime | None = None, end: datetime | None = None) -> list[Bar]:
    path = bar_data_dir() / f"{symbol}_M15.csv"
    if not path.is_file():
        raise FileNotFoundError(path)
    bars: list[Bar] = []
    with path.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            ts = datetime.strptime(row["time"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
            if start is not None and ts < start:
                continue
            if end is not None and ts > end:
                break
            bars.append(Bar(ts=ts, open=float(row["open"]), high=float(row["high"]),
                            low=float(row["low"]), close=float(row["close"]),
                            volume=float(row["volume"])))
    return bars


@dataclass(frozen=True)
class ExportTrade:
    trade_no: int
    entry_time: datetime      # naive, chart display clock (ET)
    entry_signal: str
    entry_price: float
    exit_time: datetime
    exit_signal: str
    exit_price: float
    qty: int
    net_pnl: float
    commission: float


def locate_export(leg_id: str) -> Path:
    src = phase1_source(leg_id)
    path = export_dir() / src["export_filename"]
    if not path.is_file():
        raise FileNotFoundError(path)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != src["export_sha256"]:
        raise ValueError(f"{path.name}: sha256 {digest[:12]}… != pinned {src['export_sha256'][:12]}…")
    return path


def load_export(path: Path) -> list[ExportTrade]:
    rows = list(csv.DictReader(path.open(encoding="utf-8-sig")))
    by_no: dict[int, dict[str, dict]] = {}
    for r in rows:
        kind = r["Type"].split()[0]
        by_no.setdefault(int(r["Trade number"]), {})[kind] = r
    out = []
    for n, pair in sorted(by_no.items()):
        e, x = pair.get("Entry"), pair.get("Exit")
        if e is None or x is None:
            continue   # an open trade at capture time has no exit row
        out.append(ExportTrade(
            trade_no=n,
            entry_time=datetime.strptime(e["Date and time"], "%Y-%m-%d %H:%M"),
            entry_signal=e["Signal"], entry_price=float(e["Price USD"]),
            exit_time=datetime.strptime(x["Date and time"], "%Y-%m-%d %H:%M"),
            exit_signal=x["Signal"], exit_price=float(x["Price USD"]),
            qty=int(float(e["Size (qty)"])), net_pnl=float(e["Net PnL USD"]),
            commission=float(e["Commission USD"]),
        ))
    return out


@dataclass(frozen=True)
class PortTrade:
    entry_time: datetime
    entry_kind: str
    entry_price: float
    exit_time: datetime
    exit_reason: str
    exit_price: float
    qty: int
    net_pnl: float


def port_trades(emu: TVBrokerEmulator) -> list[PortTrade]:
    def et(ts: datetime) -> datetime:
        return ts.astimezone(ET).replace(tzinfo=None)
    out = []
    for t in emu.closed_trades:
        out.append(PortTrade(et(t.entry.bar_time), t.entry.reason or t.entry.kind, t.entry.price,
                             et(t.exit.bar_time), t.exit.reason, t.exit.price, t.entry.qty, t.net_pnl))
    return sorted(out, key=lambda p: (p.entry_time, p.exit_time, p.entry_price))


@dataclass
class ParityReport:
    leg_id: str
    export_trades: int
    port_trades: int
    matched: int
    missing_in_port: int       # export trades with no (entry, exit) bar match
    extra_in_port: int
    qty_mismatches: int
    price_mismatches: int
    first_divergences: list[str] = field(default_factory=list)
    window_start: str = ""
    window_end: str = ""

    @property
    def passed(self) -> bool:
        return (self.missing_in_port == 0 and self.extra_in_port == 0
                and self.qty_mismatches == 0 and self.price_mismatches == 0)

    def summary(self) -> str:
        head = (f"{self.leg_id}: export={self.export_trades} port={self.port_trades} "
                f"matched={self.matched} missing={self.missing_in_port} extra={self.extra_in_port} "
                f"qty_mismatch={self.qty_mismatches} price_mismatch={self.price_mismatches} "
                f"window={self.window_start}..{self.window_end} -> "
                f"{'PASS' if self.passed else 'FAIL'}")
        return "\n".join([head] + ["  " + d for d in self.first_divergences])


def compare(leg_id: str, export: list[ExportTrade], port: list[PortTrade], *,
            price_tol: float, window_start: datetime, window_end: datetime,
            qty_scale: float = 1.0, max_divergences: int = 12) -> ParityReport:
    """Match on (entry bar, exit bar); export trades outside the panel window are dropped.

    ``qty_scale`` rescales the export quantity before comparing (a size-invariant
    leg captured at 2 contracts and replayed at 1 compares with 0.5).
    """
    exp = [t for t in export if window_start <= t.entry_time <= window_end and t.exit_time <= window_end]
    prt = [t for t in port if window_start <= t.entry_time <= window_end]
    exp_keys = Counter((t.entry_time, t.exit_time) for t in exp)
    prt_keys = Counter((t.entry_time, t.exit_time) for t in prt)
    matched_keys = exp_keys & prt_keys
    matched = sum(matched_keys.values())
    missing = sum((exp_keys - prt_keys).values())
    extra = sum((prt_keys - exp_keys).values())

    div: list[str] = []
    for key in sorted((exp_keys - prt_keys)):
        if len(div) < max_divergences:
            t = next(t for t in exp if (t.entry_time, t.exit_time) == key)
            div.append(f"MISSING in port: export #{t.trade_no} {t.entry_signal} {key[0]} -> "
                       f"{t.exit_signal} {key[1]} qty={t.qty}")
    for key in sorted((prt_keys - exp_keys)):
        if len(div) < max_divergences:
            t = next(t for t in prt if (t.entry_time, t.exit_time) == key)
            div.append(f"EXTRA in port: {t.entry_kind} {key[0]} -> {t.exit_reason} {key[1]} qty={t.qty}")

    qty_mm = price_mm = 0
    exp_by_key: dict[tuple, list[ExportTrade]] = {}
    for t in exp:
        exp_by_key.setdefault((t.entry_time, t.exit_time), []).append(t)
    prt_by_key: dict[tuple, list[PortTrade]] = {}
    for t in prt:
        prt_by_key.setdefault((t.entry_time, t.exit_time), []).append(t)
    for key in matched_keys:
        e_list = sorted(exp_by_key[key], key=lambda t: t.entry_price)
        p_list = sorted(prt_by_key[key], key=lambda t: t.entry_price)
        for e, p in zip(e_list, p_list):
            if round(e.qty * qty_scale) != p.qty:
                qty_mm += 1
                if len(div) < max_divergences:
                    div.append(f"QTY: export #{e.trade_no} {key[0]} qty {e.qty}x{qty_scale} vs port {p.qty}")
            if abs(e.entry_price - p.entry_price) > price_tol or abs(e.exit_price - p.exit_price) > price_tol:
                price_mm += 1
                if len(div) < max_divergences:
                    div.append(f"PRICE: export #{e.trade_no} {key[0]} {e.entry_price}->{e.exit_price} "
                               f"vs port {p.entry_price}->{p.exit_price} ({p.exit_reason})")
    return ParityReport(leg_id, len(exp), len(prt), matched, missing, extra, qty_mm, price_mm, div,
                        window_start.isoformat(), window_end.isoformat())


def panel_window_et(bars: list[Bar]) -> tuple[datetime, datetime]:
    first = bars[0].ts.astimezone(ET).replace(tzinfo=None)
    last = bars[-1].ts.astimezone(ET).replace(tzinfo=None)
    return first, last


# ── shared runner (tests + CLI) ───────────────────────────────────────────

def load_effective_inputs() -> dict | None:
    """Reconstructed effective chart inputs per leg (private JSON in the port root).

    The captured exports were produced with chart inputs that differ from the
    pinned bodies' defaults (the D26 override files are lost); the parity
    harness reconstructed them and the port root holds them as
    ``effective_inputs.json``. None when absent (public clone / bare worktree).
    """
    from c1_signal_daemon.book_adapters import port_root
    path = port_root() / "effective_inputs.json"
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def run_leg(leg_id: str, *, adapter_overrides: dict | None = None, emulator_overrides: dict | None = None,
            mode=None, quantity_rule=None, bars: list[Bar] | None = None):
    """Replay one adapter on its panel; returns (adapter, emulator, bars)."""
    from c1_signal_daemon.book_adapters import ADAPTER_BY_LEG, load_port
    from c1_signal_daemon.book_protocol import Mode
    spec = ADAPTER_BY_LEG[leg_id]
    bars = bars if bars is not None else load_panel(spec.symbol)
    mod = load_port(leg_id)
    kwargs = dict(adapter_overrides or {})
    if mode is not None:
        kwargs["mode"] = mode
    if quantity_rule is not None:
        kwargs["quantity_rule"] = quantity_rule
    adapter = mod.build(**kwargs)
    emu_kw = dict(mintick=spec.mintick, pointvalue=spec.pointvalue,
                  slippage_ticks=spec.pine_slippage_ticks,
                  commission_per_side=spec.pine_commission_per_side)
    emu_kw.update(emulator_overrides or {})
    from c1_signal_daemon.tv_broker_emulator import run_adapter
    emu = TVBrokerEmulator(leg_id=leg_id, **emu_kw)
    run_adapter(adapter, bars, emu)
    return adapter, emu, bars


def parity_for(leg_id: str, effective: dict, *, max_divergences: int = 12) -> ParityReport:
    cfg = effective[leg_id]
    _, emu, bars = run_leg(leg_id, adapter_overrides=cfg.get("adapter"),
                           emulator_overrides=cfg.get("emulator"))
    exp = load_export(locate_export(leg_id))
    ws, we = panel_window_et(bars)
    from c1_signal_daemon.book_adapters import ADAPTER_BY_LEG
    tol = ADAPTER_BY_LEG[leg_id].mintick / 4
    return compare(leg_id, exp, port_trades(emu), price_tol=tol, window_start=ws, window_end=we,
                   qty_scale=float(cfg.get("qty_scale", 1.0)), max_divergences=max_divergences)


def main(argv: list[str] | None = None) -> int:
    """Print parity verdicts and the ports' SHA-256 lines (digests + labels only)."""
    import argparse
    from c1_signal_daemon.book_adapters import ADAPTERS, port_available, port_path, port_sha256
    ap = argparse.ArgumentParser(description=main.__doc__)
    ap.add_argument("--leg", action="append", help="restrict to leg_id (repeatable)")
    a = ap.parse_args(argv)
    eff = load_effective_inputs()
    if eff is None:
        print("effective_inputs.json absent in the port root; nothing to replay")
        return 2
    rc = 0
    for spec in ADAPTERS:
        if a.leg and spec.leg_id not in a.leg:
            continue
        if not port_available(spec.leg_id):
            print(f"{spec.leg_id}: port absent at {port_path(spec.leg_id)}")
            rc = 2
            continue
        rep = parity_for(spec.leg_id, eff)
        print(rep.summary())
        print(f"  port sha256: {port_sha256(spec.leg_id)}  {port_path(spec.leg_id).name}")
        rc = rc or (0 if rep.passed else 1)
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
