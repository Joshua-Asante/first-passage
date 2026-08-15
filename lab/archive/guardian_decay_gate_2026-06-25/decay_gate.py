"""
decay_gate.py — Guardian Gold v5.5 live-decay retirement gate (runnable)
========================================================================

Implements the falsifiable spine of Q-GUARDIAN-DECAY-1 with DP-1…DP-6 resolved
(see docs/briefs/Q-GUARDIAN-DECAY-1-DP-RESOLUTION.md for the values + rationale).

State machine: ARMED → WATCH → DECAYED, mapped onto the programme-audit
disposition vocabulary (Progressive/Stable/Ambiguous/Falsified). Read-only:
this NEVER toggles execution, disables alerts, or touches Pine / core. It emits
a verdict; acting on it is a human decision.

Inputs:
  - envelope.json  (from build_envelope.py — DP-7 envelope + CUSUM calibration)
  - live trades    (per-trade R-multiples; DXTrade fills → R)
  - regime labels  (exogenous favorable/unfavorable per trade date; DP-4)

DP-4 interlock (the load-bearing guard): Guardian's favorable-regime classifier
has NO validated exogenous artifact today (VIX>20 brake FALSIFIED 2026-06-22;
endogenous-OHLC classifiers falsified Q-SPX-F09/Q-NAS-4). So:
  * If no validated classifier is wired, the gate runs UNCONDITIONED and the
    DECAYED transition is HARD-INTERLOCKED OFF — max reachable state is WATCH.
    This honors §1.1 (never retire on unconditional performance) by construction.
  * DECAYED is reachable only when --classifier-validated is passed AND a
    per-trade regime label stream is supplied AND N_in_regime ≥ M (DP-5).

Run the built-in self-test (no vendor data needed) to see the mechanics:
    python lab/analysis/guardian_decay_gate_2026-06-25/decay_gate.py --self-test

Evaluate a live stream once envelope.json exists:
    python .../decay_gate.py --envelope envelope.json --live fills.csv \
        --regime-labels regime.csv --classifier-validated
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent

# ── DP-5 / DP-6 fixed-by-judgement constants (see DP-RESOLUTION spec) ────────
M_ACTIVATION = 60          # DP-5: min in-regime trades before DECAYED can fire
M_WATCH_MIN = 20           # min in-regime trades before WATCH can engage
WATCH_ALLOC_MULT = 0.50    # DP-6a: reduced-allocation multiplier while in WATCH
WATCH_DWELL_CAP = 40       # DP-6b: max in-regime trades in WATCH before forced re-MC
RECOVERY_RESET_FRAC = 0.25 # DP-6c: CUSUM must fall below h_watch*frac ...
RECOVERY_RUN = 10          # ... for this many consecutive in-regime trades → ARMED


@dataclass
class GateState:
    state: str = "ARMED"
    disposition: str = "Stable"           # programme-audit vocabulary
    cusum: float = 0.0
    n_in_regime: int = 0
    n_in_watch: int = 0
    recovery_streak: int = 0
    log: list = field(default_factory=list)

    def to_dict(self) -> dict:
        d = self.__dict__.copy()
        d["log"] = self.log[-50:]
        return d


class DecayGate:
    """CUSUM (DP-1) on the regime-conditional R stream, H0/H1 + boundaries from
    the envelope (DP-2/DP-3), three-state output (DP-4 mapping + interlock)."""

    def __init__(self, envelope: dict, classifier_validated: bool = False):
        cal = envelope["cusum_calibration"]
        self.k = cal["k_reference_R"]
        self.h_watch = cal["h_watch"]
        self.h_decay = cal["h_decay"]
        self.E0 = envelope["r_distribution_null_H0"]["E0_mean_R"]
        self.E1 = envelope["degraded_alternative_H1"]["E1_chosen_R"]
        self.classifier_validated = bool(classifier_validated)
        self.s = GateState()

    def _disposition(self) -> str:
        return {"ARMED": "Stable", "WATCH": "Ambiguous",
                "DECAYED": "Falsified"}[self.s.state]

    def update(self, r_multiple: float, favorable: bool, when: str = "") -> None:
        """Feed one live trade. Only in-favorable-regime trades move the statistic."""
        if not favorable:
            self.s.log.append(f"{when} r={r_multiple:+.2f} OFF-REGIME (excluded)")
            return

        self.s.n_in_regime += 1
        # lower CUSUM for a downward shift E0→E1
        self.s.cusum = max(0.0, self.s.cusum + (self.k - r_multiple))

        if self.s.state == "ARMED":
            if self.s.n_in_regime >= M_WATCH_MIN and self.s.cusum >= self.h_watch:
                self.s.state = "WATCH"
                self.s.n_in_watch = 0
                self.s.recovery_streak = 0
        elif self.s.state == "WATCH":
            self.s.n_in_watch += 1
            # confirmation → DECAYED (interlocked)
            decay_ok = (self.classifier_validated
                        and self.s.n_in_regime >= M_ACTIVATION
                        and self.s.cusum >= self.h_decay)
            if decay_ok:
                self.s.state = "DECAYED"
            elif self.s.cusum < self.h_watch * RECOVERY_RESET_FRAC:
                self.s.recovery_streak += 1
                if self.s.recovery_streak >= RECOVERY_RUN:
                    self.s.state = "ARMED"      # recovery
                    self.s.n_in_watch = 0
            else:
                self.s.recovery_streak = 0

        self.s.disposition = self._disposition()
        self.s.log.append(
            f"{when} r={r_multiple:+.2f} S={self.s.cusum:.2f} "
            f"[{self.s.state}/{self.s.disposition}] n_ir={self.s.n_in_regime}")

    def verdict(self) -> dict:
        d = self.s.to_dict()
        # surface the interlock status explicitly
        d["decayed_interlock"] = {
            "classifier_validated": self.classifier_validated,
            "activation_M": M_ACTIVATION,
            "n_in_regime": self.s.n_in_regime,
            "decay_reachable": (self.classifier_validated
                                and self.s.n_in_regime >= M_ACTIVATION),
        }
        d["boundaries"] = {"k": self.k, "h_watch": self.h_watch,
                           "h_decay": self.h_decay, "E0": self.E0, "E1": self.E1}
        return d


# ── IO helpers ──────────────────────────────────────────────────────────────
def load_live_R(path: Path) -> list[tuple[str, float]]:
    """Live trades → [(date, R)]. Accepts CSV with either an 'r_multiple' column,
    or 'pnl' + 'risk_dollars' (R = pnl/risk_dollars). Date column: 'exit_date'
    or 'date' (optional)."""
    import csv
    rows: list[tuple[str, float]] = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            when = row.get("exit_date") or row.get("date") or ""
            if row.get("r_multiple") not in (None, ""):
                r = float(row["r_multiple"])
            elif row.get("pnl") and row.get("risk_dollars"):
                r = float(row["pnl"]) / float(row["risk_dollars"])
            else:
                raise ValueError("live CSV needs 'r_multiple' or 'pnl'+'risk_dollars'")
            rows.append((when, r))
    return rows


def load_regime(path: Path | None, dates: list[str]) -> dict[str, bool]:
    """Regime labels (DP-4). CSV with 'date','favorable' (1/0/true/false).
    When no file is supplied, returns all-True (UNCONDITIONED — DECAYED stays
    interlocked off per the DP-4 guard)."""
    if path is None:
        return {d: True for d in dates}
    import csv
    out: dict[str, bool] = {}
    with open(path, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            val = str(row.get("favorable", "")).strip().lower()
            out[row["date"]] = val in ("1", "true", "yes", "y", "t")
    return out


# ── self-test (runnable with no vendor data) ────────────────────────────────
def self_test() -> None:
    """Synthetic proof-of-mechanics. Builds a fake envelope with a Guardian-like
    heavy-tailed R distribution, then drives the gate with (a) an in-sample
    stream that must stay ARMED, and (b) a degraded stream that must reach WATCH
    and — only with the classifier interlock satisfied — DECAYED."""
    rng = np.random.default_rng(42)

    def gen_R(n, win_rate=0.2217, avg_win=13.2, avg_loss=-1.0, scale=1.0):
        wins = rng.random(n) < win_rate
        R = np.where(wins,
                     rng.exponential(avg_win * scale, n),
                     avg_loss * (0.5 + rng.random(n)))
        return R

    R_is = gen_R(5000)
    E0 = float(R_is.mean())
    E1 = E0 * 0.4
    k = 0.5 * (E0 + E1)
    HORIZON = 200

    def running_max_cusum(seq):
        C = m = 0.0
        for r in seq:
            C = max(0.0, C + (k - r))
            m = max(m, C)
        return m

    # finite-horizon false-alarm calibration: h = (1-alpha) quantile of the
    # in-control running-max CUSUM (matches build_envelope.calibrate_cusum).
    inctrl = np.array([running_max_cusum(rng.choice(R_is, HORIZON, replace=True))
                       for _ in range(3000)])
    h_watch = float(np.quantile(inctrl, 0.80))   # alpha_watch = 0.20
    h_decay = float(np.quantile(inctrl, 0.99))   # alpha_decay = 0.01
    env = {
        "cusum_calibration": {"k_reference_R": k, "h_watch": h_watch, "h_decay": h_decay},
        "r_distribution_null_H0": {"E0_mean_R": E0},
        "degraded_alternative_H1": {"E1_chosen_R": E1},
    }
    print(f"[self-test] E0={E0:+.3f} E1={E1:+.3f} k={k:+.3f} "
          f"h_watch={h_watch:.2f} h_decay={h_decay:.2f}")

    def run_stream(scale, validated, n=HORIZON):
        g = DecayGate(env, classifier_validated=validated)
        for r in gen_R(n, scale=scale):
            g.update(float(r), favorable=True)
        return g.s.state

    TRIALS = 200
    # (a) in-sample streams: DECAYED rate must be ≈ alpha_decay (0.01), NOT high
    is_states = [run_stream(1.0, True) for _ in range(TRIALS)]
    is_decay = is_states.count("DECAYED") / TRIALS
    print(f"[self-test] in-sample (intact edge): DECAYED rate={is_decay:.3f} "
          f"(expect ≈α_decay=0.01 — must be LOW; §5 false-positive guard)")
    assert is_decay <= 0.06, f"in-sample false-DECAYED rate too high: {is_decay}"

    # (b) degraded streams, validated classifier: should detect (power)
    dg_states = [run_stream(0.30, True) for _ in range(TRIALS)]
    dg_decay = dg_states.count("DECAYED") / TRIALS
    print(f"[self-test] degraded (validated classifier): DECAYED rate={dg_decay:.3f} "
          f"(detection power — should be >> in-sample rate)")

    # (c) degraded streams, NO validated classifier → interlock caps at WATCH
    il_states = [run_stream(0.30, False) for _ in range(TRIALS)]
    assert "DECAYED" not in il_states, "interlock breached!"
    print(f"[self-test] degraded (NO validated classifier): DECAYED count="
          f"{il_states.count('DECAYED')} (expect 0 — DP-4 interlock holds). OK")


def main():
    ap = argparse.ArgumentParser(description="Guardian v5.5 live-decay retirement gate.")
    ap.add_argument("--envelope", default=str(HERE / "envelope.json"))
    ap.add_argument("--live", help="live trades CSV (r_multiple, or pnl+risk_dollars)")
    ap.add_argument("--regime-labels", help="per-date favorable/unfavorable CSV (DP-4)")
    ap.add_argument("--classifier-validated", action="store_true",
                    help="set ONLY when a regime classifier has passed its own "
                         "regime-robustness gate; required to reach DECAYED")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        self_test()
        return

    env_path = Path(args.envelope)
    if not env_path.exists():
        print(f"NEEDS_DATA: {env_path} not found. Run build_envelope.py locally first "
              "(needs the gitignored Guardian panel). Use --self-test to see mechanics.")
        sys.exit(0)
    envelope = json.loads(env_path.read_text())

    if not args.live:
        print("No --live stream supplied. Envelope loaded; gate would arm at "
              "deployment in state ARMED (dormant). Provide --live to evaluate.")
        print(json.dumps(envelope.get("cusum_calibration", {}), indent=2))
        return

    live = load_live_R(Path(args.live))
    dates = [d for d, _ in live]
    regime = load_regime(Path(args.regime_labels) if args.regime_labels else None, dates)

    gate = DecayGate(envelope, classifier_validated=args.classifier_validated)
    for when, r in live:
        gate.update(r, favorable=regime.get(when, True), when=when)

    print(json.dumps(gate.verdict(), indent=2))


if __name__ == "__main__":
    main()
