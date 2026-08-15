"""Diagnostics for Q-PYRPARITY-1 Phase 2 qty ratios."""
from __future__ import annotations

import hashlib
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent


def entries(p: Path) -> pd.DataFrame:
    df = pd.read_csv(p)
    e = df[df["Type"].astype(str).str.contains("Entry", case=False)].copy()
    e["ts"] = pd.to_datetime(e["Date and time"])
    return e


def main() -> None:
    m0 = entries(HERE / "MYM_r070_f5ecb.csv")
    mh = entries(HERE / "MYM_r035_8d6b5.csv")
    print("MYM first 15 base Long qty r0 vs rh")
    b0 = m0[m0["Signal"] == "Long"].head(15).reset_index(drop=True)
    bh = mh[mh["Signal"] == "Long"].head(15).reset_index(drop=True)
    for i in range(15):
        r0, rh = b0.iloc[i], bh.iloc[i]
        print(
            f"  {r0['Date and time']}  {r0['Size (qty)']:g} -> {rh['Size (qty)']:g}  "
            f"ratio={rh['Size (qty)'] / r0['Size (qty)']:.4f}"
        )

    print("\nMYM qty histograms base")
    print("r0", m0[m0["Signal"] == "Long"]["Size (qty)"].value_counts().sort_index().to_dict())
    print("rh", mh[mh["Signal"] == "Long"]["Size (qty)"].value_counts().sort_index().to_dict())

    print("\nMYM first 10 adds")
    a0 = m0[m0["Signal"] == "Long Add"].head(10).reset_index(drop=True)
    ah = mh[mh["Signal"] == "Long Add"].head(10).reset_index(drop=True)
    for i in range(min(10, len(a0), len(ah))):
        r0, rh = a0.iloc[i], ah.iloc[i]
        print(
            f"  {r0['Date and time']}  {r0['Size (qty)']:g} -> {rh['Size (qty)']:g}  "
            f"ratio={rh['Size (qty)'] / r0['Size (qty)']:.4f}"
        )

    n0 = entries(HERE / "MNQ_r037_9b6c8.csv")
    nh = entries(HERE / "MNQ_r0185_b2723.csv")
    print("\nMNQ first 12 paired base")
    b0 = n0[n0["Signal"] == "Long"]
    bh = nh[nh["Signal"] == "Long"].set_index("ts")
    for _, r0 in b0.head(12).iterrows():
        ts = r0["ts"]
        if ts in bh.index:
            rh = bh.loc[ts]
            if isinstance(rh, pd.DataFrame):
                rh = rh.iloc[0]
            print(
                f"  {r0['Date and time']}  {r0['Size (qty)']:g} -> {rh['Size (qty)']:g}  "
                f"ratio={rh['Size (qty)'] / r0['Size (qty)']:.4f}"
            )
        else:
            print(f"  {r0['Date and time']}  {r0['Size (qty)']:g} -> MISSING in rh")

    print("\nMNQ qty histogram base (r0 / rh) — top bins")
    print("r0", n0[n0["Signal"] == "Long"]["Size (qty)"].describe().to_dict())
    print("rh", nh[nh["Signal"] == "Long"]["Size (qty)"].describe().to_dict())

    panel = Path("core/data/tv_exports/cme/Striker_DJ30_v4.5_MYM_CBOT_MINI_MYM1!_2026-07-11_15d8b.csv")
    new = HERE / "MYM_r070_f5ecb.csv"
    print(
        "\nMYM r0 vs panel byte-identical:",
        hashlib.sha256(panel.read_bytes()).hexdigest()
        == hashlib.sha256(new.read_bytes()).hexdigest(),
    )
    panel_n = Path("core/data/tv_exports/cme/Striker_NAS100_v1_CME_MINI_MNQ1!_2026-07-11_beabf.csv")
    new_n = HERE / "MNQ_r037_9b6c8.csv"
    print(
        "MNQ r0 vs panel byte-identical:",
        hashlib.sha256(panel_n.read_bytes()).hexdigest()
        == hashlib.sha256(new_n.read_bytes()).hexdigest(),
    )

    m_b0 = m0[m0["Signal"] == "Long"].iloc[0]
    m_bh = mh[mh["Signal"] == "Long"].iloc[0]
    ratio0 = m_bh["Size (qty)"] / m_b0["Size (qty)"]
    print("\nImplied r_half/r0 from first MYM base (raw qty):", ratio0)
    print("If r0=0.70, implied r_half =", 0.70 * ratio0)


if __name__ == "__main__":
    main()
