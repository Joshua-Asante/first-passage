"""Bar-level by-year L4 presence limb for Q-VOLREGIME-1.

Each own-range stratum must independently have n_cond >= 20; the annual
statistic is the minimum within-stratum volume lift; N_valid must be >= 7;
then at least N_valid - 2 years must be positive. Vendor bytes are verified
against tracked SHA256SUMS values before scoring.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
DATA = REPO / "core" / "data" / "bar_data"
EXPECTED = {
    "MNQ": "6c86f41a17b7dfce05baa205a4147b7504f3ce1eb14a3b03b994aa090fa7e00a",
    "MYM": "24e169528f7ea6693b75c71c3195edf6a04f3a26c6b6dff0f2e9c623fd597a58",
}
YEAR_MIN_NCOND = 20


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tod_threshold(values: np.ndarray, slots: np.ndarray, window: int) -> np.ndarray:
    """Trailing same-slot median (strict prior). Guards `med > 0`, matching the
    reference construction's div-by-zero guard (c3_volume_regime.py::tod_ratio)
    -- a degenerate all-zero window leaves the threshold NaN (excluded) rather
    than silently gating on 0."""
    out = np.full(len(values), np.nan)
    history: dict[int, list[float]] = {}
    for i, (value, slot) in enumerate(zip(values, slots)):
        hist = history.setdefault(int(slot), [])
        if len(hist) >= window:
            med = float(np.median(hist[-window:]))
            if med > 0:
                out[i] = med
        hist.append(float(value))
    return out


def prepare(symbol: str) -> tuple[pd.DataFrame, dict]:
    path = DATA / f"{symbol}_M15.csv"
    if not path.is_file():
        raise RuntimeError(
            f"{symbol} vendor panel absent: {path}; restore the hash-pinned file before scoring"
        )
    actual_hash = sha256(path)
    if actual_hash != EXPECTED[symbol]:
        raise RuntimeError(f"{symbol} hash mismatch: {actual_hash}")

    raw = pd.read_csv(path)
    raw["time"] = pd.to_datetime(raw["time"], utc=True)
    raw = raw.sort_values("time").drop_duplicates("time", keep="last").reset_index(drop=True)
    et = raw["time"].dt.tz_convert("America/New_York")
    slots = (et.dt.hour * 60 + et.dt.minute).to_numpy()
    trading_day = et.dt.normalize() + pd.to_timedelta((slots >= 18 * 60).astype(int), unit="D")

    if symbol == "MYM":  # frozen stage-1 exclusion of final truncated session
        keep = trading_day < trading_day.max()
        raw = raw.loc[keep].reset_index(drop=True)
        slots = slots[keep.to_numpy()]
        trading_day = trading_day.loc[keep].reset_index(drop=True)

    window = 60 if symbol == "MNQ" else 20
    volume = raw["volume"].to_numpy(float)
    bar_range = (raw["high"] - raw["low"]).to_numpy(float)
    volume_threshold = tod_threshold(volume, slots, window)
    range_threshold = tod_threshold(bar_range, slots, window)

    volume_cmp = np.greater_equal if symbol == "MNQ" else np.greater
    bias_volume = np.where(
        np.isnan(volume_threshold), np.nan, volume_cmp(volume, volume_threshold).astype(float)
    )
    bias_range = np.where(
        np.isnan(range_threshold), np.nan, np.greater(bar_range, range_threshold).astype(float)
    )
    outcome = np.full(len(raw), np.nan)
    outcome[:-1] = np.where(
        ~np.isnan(range_threshold[1:]),
        np.greater(bar_range[1:], range_threshold[1:]).astype(float),
        np.nan,
    )

    scored = (~np.isnan(bias_volume)) & (~np.isnan(bias_range)) & (~np.isnan(outcome))
    frame = pd.DataFrame(
        {
            "time_utc": raw.loc[scored, "time"].reset_index(drop=True),
            "trading_day": trading_day.loc[scored].reset_index(drop=True),
            "year": trading_day.dt.year.to_numpy()[scored].astype(int),
            "bias_volume": bias_volume[scored].astype(int),
            "bias_range": bias_range[scored].astype(int),
            "outcome": outcome[scored].astype(int),
        }
    )
    return frame, {
        "csv": path.relative_to(REPO).as_posix(),
        "sha256": actual_hash,
        "window_same_slot_prior_observations": window,
        "n_scored": int(len(frame)),
        "span_utc": [str(raw["time"].min()), str(raw["time"].max())],
    }


def score_l4(frame: pd.DataFrame) -> dict:
    by_year = {}
    for year, year_frame in frame.groupby("year", sort=True):
        strata = {}
        for stratum in (0, 1):
            ss = year_frame[year_frame["bias_range"] == stratum]
            hi = ss.loc[ss["bias_volume"] == 1, "outcome"]
            lo = ss.loc[ss["bias_volume"] == 0, "outcome"]
            lift = float(hi.mean() - lo.mean()) if len(hi) and len(lo) else None
            strata[str(stratum)] = {
                "n_cond": int(len(hi)),
                "n_ref": int(len(lo)),
                "rate_cond": float(hi.mean()) if len(hi) else None,
                "rate_ref": float(lo.mean()) if len(lo) else None,
                "lift": lift,
            }
        qualifies = all(strata[str(s)]["n_cond"] >= YEAR_MIN_NCOND for s in (0, 1))
        lifts = [strata[str(s)]["lift"] for s in (0, 1)]
        min_lift = min(lifts) if all(value is not None for value in lifts) else None
        by_year[str(int(year))] = {
            "strata": strata,
            "qualifies": qualifies,
            "min_lift": min_lift,
            "passes": bool(qualifies and min_lift is not None and min_lift > 0),
        }

    valid = [row for row in by_year.values() if row["qualifies"]]
    n_valid = len(valid)
    n_pass = sum(row["passes"] for row in valid)
    required = n_valid - 2 if n_valid >= 7 else None
    verdict = "AMBIGUOUS" if n_valid < 7 else ("PASS" if n_pass >= required else "FAIL")
    return {
        "year_min_n_cond_per_stratum": YEAR_MIN_NCOND,
        "by_year": by_year,
        "l4": {"n_valid": n_valid, "n_pass": n_pass, "required": required, "verdict": verdict},
    }


def main() -> None:
    results = {
        "method": "Q-VOLREGIME-1 bar-level by-year L4; min lift across own-range strata",
        "instruments": {},
    }
    for symbol in ("MNQ", "MYM"):
        frame, metadata = prepare(symbol)
        results["instruments"][symbol] = {"input": metadata, **score_l4(frame)}
        l4 = results["instruments"][symbol]["l4"]
        print(
            f"{symbol}: n_valid={l4['n_valid']} n_pass={l4['n_pass']} "
            f"required={l4['required']} L4={l4['verdict']}"
        )
    output = HERE / "byyear_l4_results.json"
    output.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
