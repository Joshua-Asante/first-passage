"""Source-derived cash ledger arithmetic shared by producer and verifier."""
from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal
from .book_policy import FIRM_RULES, TIER
from .account_close_evidence import AssemblyError, CashRow, COST_TYPES, TRADE_TYPE, FUND_TYPE, ET, account_session_date, session_id_for

STARTING_BALANCE = Decimal(str(FIRM_RULES[TIER]["starting_balance"]))

@dataclass(frozen=True)
class Ledger:
    basis: Decimal
    fund_row: CashRow
    sessions: dict[date, dict]           # per account session: gross, costs, net_after, rows
    equity_after: dict[date, Decimal]    # running net after each session with activity
    peak: Decimal
    unknown_rows: int
    unlinked_fee_rows: int
    adjustments_abs_total: Decimal
    classified: dict[str, int]


def reconcile(rows: list[CashRow]) -> Ledger:
    """Nominal funding basis first, then trade P&L and transaction-linked costs per account session."""
    funds = [r for r in rows if r.kind == FUND_TYPE]
    if not funds:
        raise AssemblyError("no fund transaction establishes the nominal basis")
    fund = min(funds, key=lambda r: r.ts_utc)
    if fund.delta != STARTING_BALANCE or fund.amount_after != STARTING_BALANCE:
        raise AssemblyError("first fund transaction is not the nominal starting balance")
    if any(r.ts_utc < fund.ts_utc for r in rows):
        raise AssemblyError("cash activity precedes the funding basis")
    sessions: dict[date, dict] = {}
    running = STARTING_BALANCE
    unknown = unlinked = 0
    adjustments = Decimal(0)
    classified: dict[str, int] = {}
    peak = STARTING_BALANCE
    for row in rows:
        if row is fund:
            classified[FUND_TYPE] = classified.get(FUND_TYPE, 0) + 1
            continue
        day = account_session_date(row.ts_utc)
        if day is None:
            raise AssemblyError(f"cash row outside any account session at transaction {row.transaction_id[-4:]}; "
                                "explicit adjudication required")
        bucket = sessions.setdefault(day, {"gross": Decimal(0), "costs": {k: Decimal(0) for k in COST_TYPES.values()},
                                           "rows": 0, "trade_rows": 0, "last_ts_utc": row.ts_utc})
        bucket["rows"] += 1
        bucket["last_ts_utc"] = max(bucket["last_ts_utc"], row.ts_utc)
        classified[row.kind] = classified.get(row.kind, 0) + 1
        if row.kind == TRADE_TYPE:
            bucket["gross"] += row.delta
            bucket["trade_rows"] += 1
        elif row.kind in COST_TYPES:
            if not row.contract:
                unlinked += 1
            bucket["costs"][COST_TYPES[row.kind]] += -row.delta
        elif row.kind == FUND_TYPE:
            adjustments += abs(row.delta)
        else:
            unknown += 1
            adjustments += abs(row.delta)
        running += row.delta
        if running != row.amount_after:
            raise AssemblyError(f"running balance disagrees with the report at transaction {row.transaction_id[-4:]}")
    equity_after: dict[date, Decimal] = {}
    running = STARTING_BALANCE
    for day in sorted(sessions):
        bucket = sessions[day]
        running = running + bucket["gross"] - sum(bucket["costs"].values())
        bucket["net_after"] = running
        equity_after[day] = running
        peak = max(peak, running)
    return Ledger(STARTING_BALANCE, fund, sessions, equity_after, peak, unknown, unlinked, adjustments, classified)


def equity_at_end_of(ledger: Ledger, day: date) -> Decimal:
    value = ledger.basis
    for session_day in sorted(ledger.equity_after):
        if session_day <= day:
            value = ledger.equity_after[session_day]
    return value


def check_balance_history(ledger: Ledger, balance: list[tuple[date, Decimal, Decimal]]) -> dict:
    """Every venue balance row must equal the reconciled equity at the end of that trade date."""
    mismatches = 0
    for day, total, _ in balance:
        if equity_at_end_of(ledger, day) != total:
            mismatches += 1
    return {"rows": len(balance), "mismatches": mismatches, "first_date": balance[0][0].isoformat(),
            "last_date": balance[-1][0].isoformat()}


def labelled_session(r: CashRow) -> str:
    # In-session rows were mapped by reconcile(); the nominal funding row precedes every session
    # and is labelled with the first account day after it.
    day = account_session_date(r.ts_utc)
    if day is None:
        day = r.ts_utc.astimezone(ET).date() + timedelta(days=1)
        while day.weekday() >= 5:
            day += timedelta(days=1)
    return session_id_for(day)



def transactions_for(rows: list[CashRow]) -> list[dict]:
    return [{"id": r.transaction_id, "sha256": r.content_sha256, "session_id": labelled_session(r)}
            for r in rows]
