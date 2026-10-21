"""Path-to-first-payout simulator for futures prop programs.

Strategy: intraday Brownian P&L with annualised Sharpe S and daily vol sd (at full-day
exposure), optional self-imposed daily stop (-stop) and daily take (+take) that end the
trading day early. Program: eval phase then funded phase, with resets/re-buys until the
first payout or the horizon (trading days) runs out.
"""
import numpy as np, math
from dataclasses import dataclass, field

SUB = 26  # intraday sub-steps (15-min bars over a 6.5h session)

@dataclass
class Phase:
    target: float = 0.0          # eval profit target (0 for funded)
    dd: float = 3000.0           # max drawdown distance
    dd_type: str = "eod"         # "eod" trailing on closes, "intraday" trailing on intraday peak, "static"
    lock: float | None = None    # floor stops trailing once it reaches this level (rel. to start), None = never
    dll: float | None = None     # daily loss limit
    dll_hard: bool = False       # True: breach ends account; False: day stops
    cons: float | None = None    # best day <= cons * profit (eval: at pass; funded: at payout, over cycle)
    min_days: int = 0
    # funded payout gate
    win_days: int = 0            # winning days needed per cycle
    win_thr: float = 0.0         # $ threshold for a winning day
    buffer: float = 0.0          # profit above start required before a request
    cap: float = 1e12            # max payout per request
    frac: float = 1.0            # max fraction of profit requestable
    min_pay: float = 0.0
    split: float = 0.9
    excess: bool = False         # True: requestable = profit - buffer (balance must stay above buffer)

@dataclass
class Program:
    name: str
    price: float
    reset: float
    activation: float
    ev: Phase | None  # None = instant funding (no evaluation)
    fd: Phase
    max_contracts_note: str = ""
    monthly: float = 0.0  # subscription charged per 21 eval trading days beyond the first month

def _day(rng, n, mu, s, stop, take):
    """Simulate one trading day for n paths; returns (path array (n,SUB+1) cumulative, final pnl)."""
    inc = mu / SUB + s * rng.standard_normal((n, SUB))
    cum = np.concatenate([np.zeros((n, 1)), np.cumsum(inc, axis=1)], axis=1)
    if stop is not None or take is not None:
        hit = np.zeros_like(cum, dtype=bool)
        if stop is not None: hit |= cum <= -stop
        if take is not None: hit |= cum >= take
        first = np.where(hit.any(1), hit.argmax(1), SUB)
        idx = np.arange(SUB + 1)[None, :]
        frozen = np.take_along_axis(cum, first[:, None], 1)
        cum = np.where(idx > first[:, None], frozen, cum)
    return cum

def run_phase(rng, ph, n, mu, s, stop, take, days_left, funded):
    """Run one attempt of a phase for n paths. Returns outcome (1 success,0 fail,-1 timeout), days used, payout amount."""
    eq = np.zeros(n); peak = np.zeros(n); best = np.zeros(n); wins = np.zeros(n, int)
    out = np.full(n, -1); used = days_left.copy(); pay = np.zeros(n)
    act = days_left > 0
    maxd = int(days_left.max()) if n else 0
    if ph.dll is not None and not ph.dll_hard:  # soft DLL acts as a forced daily stop
        stop = ph.dll if stop is None else min(stop, ph.dll)
    for d in range(1, maxd + 1):
        act &= d <= days_left
        if not act.any(): break
        cum = _day(rng, n, mu, s, stop, take)
        path = eq[:, None] + cum
        if ph.dd_type == "static":
            floor = np.full(n, -ph.dd)
            fl_path = np.broadcast_to(floor[:, None], path.shape)
        elif ph.dd_type == "eod":
            floor = peak - ph.dd
            if ph.lock is not None: floor = np.minimum(floor, ph.lock)
            fl_path = np.broadcast_to(floor[:, None], path.shape)
        else:  # intraday trailing
            run_pk = np.maximum(peak[:, None], np.maximum.accumulate(path, axis=1))
            fl_path = run_pk - ph.dd
            if ph.lock is not None: fl_path = np.minimum(fl_path, ph.lock)
        breach = (path <= fl_path).any(1)
        dayp = cum[:, -1]
        if ph.dll is not None and ph.dll_hard:
            breach |= (cum <= -ph.dll).any(1)
        f = act & breach
        out[f] = 0; used[f] = d; act[f] = False
        ok = act
        eq[ok] += dayp[ok]
        if ph.dd_type == "intraday":
            peak[ok] = np.maximum(peak[ok], path[ok].max(1))
        else:
            peak[ok] = np.maximum(peak[ok], eq[ok])
        best[ok] = np.maximum(best[ok], dayp[ok])
        wins[ok & (dayp >= max(ph.win_thr, 1e-9))] += 1
        if not funded:
            p = ok & (eq >= ph.target) & (d >= ph.min_days)
            if ph.cons is not None: p &= best <= ph.cons * eq
        else:
            p = ok & (wins >= ph.win_days) & (eq >= ph.buffer) & (d >= ph.min_days)
            if ph.cons is not None: p &= best <= ph.cons * np.maximum(eq, 1e-9)
            base = (eq - ph.buffer) if ph.excess else eq
            amt = np.minimum(ph.cap, ph.frac * np.maximum(base, 0))
            p &= amt >= max(ph.min_pay, 1.0)
            pay[p] = ph.split * amt[p]
        out[p] = 1; used[p] = d; act[p] = False
    return out, used, pay

def first_payout(prog, S, sd, stop=None, take=None, sd_f=None, stop_f=None, take_f=None,
                 H=120, N=6000, seed=1, min_net=0.0):
    """Buy evals (reset on fail), activate when passed, trade funded until first payout.
    Returns dict: P(first payout within H days), mean cost, median days, mean first payout,
    and per-attempt eval pass rate."""
    rng = np.random.default_rng(seed)
    if min_net > 0:  # trader waits until the request nets at least min_net
        from dataclasses import replace
        prog = replace(prog, fd=replace(prog.fd, min_pay=max(prog.fd.min_pay, min_net / prog.fd.split)))
    sd_f = sd if sd_f is None else sd_f
    stop_f = stop if stop_f is None else stop_f
    take_f = take if take_f is None else take_f
    mu_e, s_e = S * sd / math.sqrt(252), sd / math.sqrt(SUB)
    mu_f, s_f = S * sd_f / math.sqrt(252), sd_f / math.sqrt(SUB)
    left = np.full(N, H); cost = np.zeros(N); done = np.zeros(N, bool); tdays = np.full(N, np.nan)
    first_pay = np.zeros(N); stage = np.zeros(N, int)  # 0 eval, 1 funded
    if prog.ev is None:
        stage[:] = 1; cost += prog.price
    fresh_eval = np.ones(N, bool)
    ev_try = 0; ev_pass = 0; ev_days = np.zeros(N)
    active = np.ones(N, bool)
    for _ in range(200):
        ix = np.where(active & (stage == 0))[0]
        if len(ix):
            cost[ix] += np.where(fresh_eval[ix], prog.price, prog.reset)
            o, u, _ = run_phase(rng, prog.ev, len(ix), mu_e, s_e, stop, take, left[ix].copy(), False)
            ev_try += len(ix); ev_pass += (o == 1).sum()
            left[ix] -= u; ev_days[ix] += u
            ps = o == 1; stage[ix[ps]] = 1; cost[ix[ps]] += prog.activation
            fresh_eval[ix[~ps]] = False
            active[ix[o == -1]] = False
        jx = np.where(active & (stage == 1))[0]
        if len(jx):
            o, u, pay = run_phase(rng, prog.fd, len(jx), mu_f, s_f, stop_f, take_f, left[jx].copy(), True)
            left[jx] -= u
            ps = o == 1
            done[jx[ps]] = True; active[jx[ps]] = False; first_pay[jx[ps]] = pay[ps]
            tdays[jx[ps]] = H - left[jx[ps]]
            bust = o == 0
            if prog.ev is None:
                cost[jx[bust]] += prog.price
            else:
                stage[jx[bust]] = 0; fresh_eval[jx[bust]] = True
            active[jx[o == -1]] = False
        active &= left > 0
        if not active.any(): break
    if prog.monthly: cost += prog.monthly * np.maximum(0, np.ceil(ev_days / 21) - 1)
    return dict(p_pay=done.mean(), cost=cost.mean(), cost_paid=cost[done].mean() if done.any() else np.nan,
                days_med=np.nanmedian(tdays) if done.any() else np.nan,
                first_pay=first_pay[done].mean() if done.any() else 0.0,
                net=(first_pay - cost).mean(), ev_pass=ev_pass / max(ev_try, 1))
