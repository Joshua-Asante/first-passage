"""Personal-account running-peak halt-and-flatten (ADR 2026-10-09 Decision 4, owed item 7).

Equity at or past ``max_dd_pct`` below its running peak halts new entries and
requires a flatten; only an operator GO resumes (after a confirmed flatten).
Keyed (portfolio_id, tier); the threshold is read from FIRM_RULES[tier], never a
literal here, and is not a dd_protection/POLICY_REGISTRY instance.

Fail-closed: missing, corrupt, foreign or stale state and any persist failure
block entries. Callers must feed every equity read, intraday lows included; the
latch makes a recovered close irrelevant. Single writer per state file. The GO
is checked for shape and single use, not for a signature. Not wired to the rail
(card P4): this module places no orders; ``flatten`` calls an injected executor.
"""
from __future__ import annotations

import json
import math
import os
import sys
import tempfile
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT / "core") not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT / "core"))

import firm_rules  # noqa: E402

SCHEMA = "personal_drawdown_halt/v1"
TIER = "Personal_Tradovate"
_FIELDS = {"schema", "account", "portfolio_id", "tier", "threshold", "peak", "state",
           "flatten", "incidents", "resumes"}
_FLATTEN = {"RUNNING": {"NOT_REQUIRED"}, "HALTED": {"REQUIRED", "FAILED", "CONFIRMED"}}


class HaltStateError(RuntimeError):
    """State unavailable or invalid; entries are refused."""


def _now():
    return datetime.now(timezone.utc).isoformat()


def _threshold(tier):
    return str(Fraction(str(firm_rules.FIRM_RULES[tier]["max_dd_pct"])) / 100)


def _equity(value):
    """Finite positive float, else None. The single numeric conversion for state
    ``peak`` and caller equity, so an int beyond the float range (a valid JSON
    10**309) is invalid rather than an escaping OverflowError."""
    if type(value) not in (int, float):
        return None
    try:
        value = float(value)
    except OverflowError:
        return None
    return value if math.isfinite(value) and value > 0 else None


def _text(value):
    return type(value) is str and bool(value.strip())


def _atomic_write(path, state):
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=path.name, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(state, fh, sort_keys=True)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, path)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise
    _fsync_directory(path.parent)


def _fsync_directory(directory):
    """Make the rename durable (POSIX: fsync the parent directory). Windows has no
    directory handle via ``os.open``; NTFS journals the rename's metadata, and the
    rail host is Linux, where this runs."""
    if os.name == "posix":
        fd = os.open(directory, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)


_FLAT_KEYS = frozenset({"open_positions", "working_orders", "order_path_closed"})


def flat_and_closed(evidence):
    """Flat for halt or account switch: zero open positions, zero working orders and
    no path to submit a delayed entry. Anything else, malformed included, is False
    (uncertainty blocks)."""
    return (type(evidence) is dict and set(evidence) == _FLAT_KEYS
            and type(evidence["open_positions"]) is int and evidence["open_positions"] == 0
            and type(evidence["working_orders"]) is int and evidence["working_orders"] == 0
            and evidence["order_path_closed"] is True)


class PersonalDrawdownHalt:
    def __init__(self, path, *, account, portfolio_id, tier=TIER):
        self.path = Path(path)
        self.account, self.portfolio_id, self.tier = account, portfolio_id, tier
        self._poisoned = False

    @classmethod
    def initialize(cls, path, *, account, portfolio_id, starting_equity, tier=TIER):
        """Create RUNNING state at ``starting_equity``; never overwrites existing state."""
        halt = cls(path, account=account, portfolio_id=portfolio_id, tier=tier)
        peak = _equity(starting_equity)
        if halt.path.exists() or peak is None or not (_text(account) and _text(portfolio_id)):
            raise HaltStateError("refusing to initialize: state exists or inputs invalid")
        halt._write({"schema": SCHEMA, "account": account, "portfolio_id": portfolio_id,
                     "tier": tier, "threshold": _threshold(tier), "peak": peak,
                     "state": "RUNNING", "flatten": "NOT_REQUIRED", "incidents": [],
                     "resumes": []})
        return halt

    def _write(self, state):
        try:
            _atomic_write(self.path, state)
        except OSError as exc:
            self._poisoned = True
            raise HaltStateError("halt state could not be persisted") from exc

    def snapshot(self):
        if self._poisoned:
            raise HaltStateError("halt state unpersisted in this process")
        try:
            s = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise HaltStateError("halt state unavailable") from exc
        try:
            valid = self._valid(s)
        except (TypeError, KeyError, AttributeError):
            valid = False
        if not valid:
            raise HaltStateError("halt state invalid, foreign or stale")
        return s

    def _valid(self, s):
        if type(s) is not dict or set(s) != _FIELDS or not all(
                type(s[k]) is str for k in ("schema", "account", "portfolio_id", "tier",
                                            "threshold", "state", "flatten")):
            return False
        return not (s["schema"] != SCHEMA
                or (s["account"], s["portfolio_id"], s["tier"]) != (self.account, self.portfolio_id, self.tier)
                or s["threshold"] != _threshold(self.tier) or _equity(s["peak"]) is None
                or s["flatten"] not in _FLATTEN.get(s["state"], ())
                or type(s["incidents"]) is not list or type(s["resumes"]) is not list
                or not all(type(r) is dict and _text(r.get("go_id")) for r in s["resumes"]))

    def entry_permitted(self):
        try:
            return self.snapshot()["state"] == "RUNNING"
        except HaltStateError:
            return False

    def flatten_required(self):
        try:
            return self.snapshot()["flatten"] in ("REQUIRED", "FAILED")
        except HaltStateError:
            return True

    def _breached(self, peak, equity):
        return round((peak - equity) / peak, 6) >= float(Fraction(_threshold(self.tier)))

    def observe(self, equity):
        """Record one equity read; halt on breach or invalid equity. Returns state."""
        s = self.snapshot()
        value = _equity(equity)
        if s["state"] == "RUNNING":
            reason = "equity_invalid" if value is None else (
                "drawdown" if self._breached(s["peak"], value) else None)
            if reason is None:
                s["peak"] = max(s["peak"], value)
            else:
                s.update(state="HALTED", flatten="REQUIRED")
                s["incidents"].append({"reason": reason, "equity": value, "peak": s["peak"], "at": _now()})
            self._write(s)
        return s

    def flatten(self, executor):
        """Call ``executor(account) -> evidence`` while a flatten is owed.

        Only ``flat_and_closed(evidence)`` confirms; anything else (exception,
        positions or working orders left, an open order path, malformed evidence)
        records FAILED and leaves the flatten owed. True when confirmed."""
        s = self.snapshot()
        if s["state"] == "RUNNING" or s["flatten"] == "CONFIRMED":
            return True
        try:
            evidence = executor(self.account)
        except Exception:
            evidence = None
        s["flatten"] = "CONFIRMED" if flat_and_closed(evidence) else "FAILED"
        self._write(s)
        return s["flatten"] == "CONFIRMED"

    def resume(self, go, *, current_equity):
        """Operator GO resumes a flattened halt. ``rebase_peak`` must be explicit:
        False carries the running peak, ratcheted to ``current_equity`` (refused while still breached), True resets
        it to ``current_equity``. Each go_id resumes once. True when resumed."""
        s = self.snapshot()
        value = _equity(current_equity)
        if (s["state"] != "HALTED" or s["flatten"] != "CONFIRMED" or value is None
                or type(go) is not dict or not _text(go.get("go_id")) or not _text(go.get("operator"))
                or go.get("account") != self.account or go.get("portfolio_id") != self.portfolio_id
                or type(go.get("rebase_peak")) is not bool
                or go["go_id"] in {r["go_id"] for r in s["resumes"]}):
            return False
        if go["rebase_peak"]:
            s["peak"] = value
        elif self._breached(s["peak"], value):
            return False
        else:
            s["peak"] = max(s["peak"], value)
        s.update(state="RUNNING", flatten="NOT_REQUIRED")
        s["resumes"].append({"go_id": go["go_id"], "operator": go["operator"],
                             "rebase_peak": go["rebase_peak"], "equity": value, "at": _now()})
        self._write(s)
        return True
