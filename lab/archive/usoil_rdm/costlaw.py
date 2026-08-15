# Cost-law pre-flight for short-only USOIL Aegis-style fader
# Master eq (risk-based sizing; contract/lot size cancels out):
#   Cost_R = (x_price + c*P) / (k * ATR)
# where x_price = round-trip (spread + 2*slippage) in PRICE units,
#       c = round-trip commission as fraction of notional,
#       P = oil price, k = stop ATR-multiple, ATR = $ ATR at execution TF.

# ---- Oil cost structure (Pepperstone/Alchemy spot CFD) ----
# Spot WTI CFD: SPREAD-ONLY, no notional commission (confirmed Pepperstone commodities).
# Even a worst-case FX-equivalent commission contributes negligibly; quantify it:
c_fx_equiv = 0.00007   # ~$3.5/side/100k round-trip as fraction of notional
for P in [85, 95, 110, 130]:
    print(f"  commission term c*P at P=${P}: {c_fx_equiv*P:.4f} price units  (vs spread 0.04-0.16)")
print()

# ---- x_price scenarios (round-trip, price units). Entries cluster in volatile regime. ----
x_scenarios = {
    "calm (advertised, NOT realistic for spikes)": 0.02 + 2*0.01,   # 0.04
    "elevated session (realistic base case)":       0.04 + 2*0.02,   # 0.08
    "spike / fast market (stress case)":            0.08 + 2*0.04,   # 0.16
}

# ---- Per-TF ATR in the ELEVATED regime entries actually occur in ($ ATR) ----
# Anchored to current WTI ~ $84, monthly range ~$35, daily moves $3-5 in this regime.
tf_atr_elevated = {
    "15m": 0.70,
    "1H":  1.40,
    "4H":  3.00,
    "1D":  4.00,
}

k_grid = [1.5, 2.0, 2.5, 3.0]

def band(cr):
    if cr <= 0.03: return "comfortable"
    if cr <= 0.06: return "acceptable"
    if cr <= 0.10: return "MARGINAL"
    return "CRIPPLING"

print("="*78)
print("Cost_R = x_price / (k*ATR), spread-only (c~0). Bands: <=.03 comfortable, ")
print(" <=.06 acceptable, <=.10 marginal, >.10 crippling (the USDCAD-15m failure zone)")
print("="*78)

for xname, x in x_scenarios.items():
    print(f"\n### x_price = {x:.2f}  [{xname}]")
    header = "TF/ATR".ljust(12) + "".join([f"k={k}".rjust(11) for k in k_grid])
    print(header)
    for tf, atr in tf_atr_elevated.items():
        row = f"{tf} (${atr:.2f})".ljust(12)
        for k in k_grid:
            cr = x / (k*atr)
            row += f"{cr:.3f}".rjust(11)
        print(row)
    # also show the band for the realistic mid-k=2.5 column
    print("   band @k=2.5:  " + " | ".join([f"{tf}:{band(x/(2.5*atr))}" for tf,atr in tf_atr_elevated.items()]))

# ---- Stop-distance floor: min S ($) to keep Cost_R <= ceiling, per x_price ----
print("\n" + "="*78)
print("Stop-distance FLOOR: minimum stop S($) to hold Cost_R <= target, per x_price")
print("  S_min = x_price / Cost_R_ceiling")
print("="*78)
for ceil in [0.05, 0.03]:
    print(f"\n  target Cost_R <= {ceil}:")
    for xname, x in x_scenarios.items():
        Smin = x/ceil
        # which TF/k reaches it (using elevated ATR)
        reach = []
        for tf, atr in tf_atr_elevated.items():
            kneed = Smin/atr
            reach.append(f"{tf}: need k>={kneed:.1f}")
        print(f"    x={x:.2f} -> S_min=${Smin:.2f}  ({xname.split('(')[0].strip()})")
        print(f"        {'  |  '.join(reach)}")

# ---- Lot-size sanity (NOT the gate; just reasonableness) ----
print("\n" + "="*78)
print("Lot-size sanity check (1 lot=1000bbl=$1000/pt; risk 1.5% x $200k = $3,000)")
print("="*78)
R = 0.015*200000
for S in [1.5, 2.0, 3.0, 4.0, 6.0, 8.0]:
    lots = R/(S*1000)
    print(f"  stop S=${S:.1f}  ->  {lots:.2f} lots   (notional @P=$90: ${lots*1000*90:,.0f})")
