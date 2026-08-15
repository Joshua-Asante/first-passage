"""Cheap falsifier for the MCL TAS delta-extraction probe (pre-authoring, $0, K=0).

Question: BEFORE scoping a probe, is the delta it would have to find even in the
range of any causal-public delta this estate has ever admitted?

Inputs are all frozen/committed constants, cited inline. No market data read.
"""

# --- Frozen inputs (owners cited; nothing re-derived here) ---
COST_LAW_MULTIPLE = 4.0        # harvest Req 5, operator-frozen COST-MULT-4X
RT_USD            = 2.90       # PREREG F3 basis: $0.95/side + 1 tick total_rt, MCL
TICK_VALUE        = 1.00       # MCL: $0.01/bbl x 100 bbl
STOP_TICKS        = 20         # entry JSON: shallowest OPEN rung for MCL
BBL_PER_CONTRACT  = 100
N_COMMITTED       = 251        # PREREG F5: MCL Stage-1 own-panel N

# Estate's causal-public delta record (bp/event), for the reachability comparison.
# All are *admissible* readings, i.e. informed-flow components already stripped.
ESTATE_CAUSAL_PUBLIC_BP = {
    "gold PM-fix, generous top (R8, incl. untimeable end-block)": 3.21,
    "gold PM-fix, conservative (R8)":                             1.32,
    "D5 intraday momentum, cohort-implied":                       2.97,
    "H-OD-1 ES overnight drift, cohort":                          1.50,
    "H-FBEIA-1 CL-EIA (same instrument family)":                 -1.16,
}

# Panel-era WTI price bases. Req 5 mandates the IS-panel basis, never present day.
PRICE_BASES = {
    "2023 panel (MCL cache era), approx median": 78.0,
    "conservative low":                          70.0,
    "2022 elevated":                             95.0,
    "implausible high (stress the hurdle down)": 120.0,
}

hurdle_ticks   = COST_LAW_MULTIPLE * RT_USD / TICK_VALUE
hurdle_usd_ct  = hurdle_ticks * TICK_VALUE
hurdle_per_bbl = hurdle_usd_ct / BBL_PER_CONTRACT
required_R     = hurdle_ticks / STOP_TICKS

print("=" * 74)
print("MCL TAS delta-extraction probe -- pre-authoring cheap falsifier")
print("=" * 74)
print(f"\nReq-5 hurdle  = {COST_LAW_MULTIPLE} x RT ${RT_USD} / tick_value ${TICK_VALUE}")
print(f"              = {hurdle_ticks:.2f} ticks/event"
      f"  = ${hurdle_usd_ct:.2f}/contract = ${hurdle_per_bbl:.4f}/bbl")
print(f"Required gross in R of the cell's own {STOP_TICKS}-tick stop = {required_R:.3f}R")
print(f"  (EM1 net edge floor is 0.40R; F4 K-COST kills above 0.85R -> cell stays OPEN,")
print(f"   but the COST hurdle alone already demands more than the EM1 shape floor.)")

print(f"\n--- Required delta in bp/event, by panel-era price basis ---")
req_bp = {}
for label, price in PRICE_BASES.items():
    bp = hurdle_per_bbl / price * 10_000
    req_bp[label] = bp
    print(f"  P = ${price:6.2f}/bbl   ->  required delta = {bp:6.2f} bp/event   [{label}]")

primary_bp = req_bp["2023 panel (MCL cache era), approx median"]
min_bp     = min(req_bp.values())

print(f"\n--- Estate's causal-public delta record (bp/event) ---")
for label, bp in sorted(ESTATE_CAUSAL_PUBLIC_BP.items(), key=lambda kv: -kv[1]):
    print(f"  {bp:+6.2f} bp   {label}")
ceiling = max(ESTATE_CAUSAL_PUBLIC_BP.values())
print(f"\n  Estate ceiling (largest causal-public delta ever admitted) = {ceiling:.2f} bp")

print(f"\n--- Reachability verdict ---")
print(f"  Required (2023 panel basis) : {primary_bp:.2f} bp")
print(f"  Required (most generous basis, implausible $120 oil) : {min_bp:.2f} bp")
print(f"  Estate ceiling              : {ceiling:.2f} bp")
print(f"  Gap at panel basis          : {primary_bp / ceiling:.2f}x over the ceiling")
print(f"  Gap at the MOST generous basis : {min_bp / ceiling:.2f}x over the ceiling")

verdict = "FALSIFIER FIRES" if min_bp > ceiling else "falsifier does not fire"
print(f"\n  => {verdict}: the probe must find a causal-public delta "
      f"{min_bp/ceiling:.1f}x-{primary_bp/ceiling:.1f}x larger than")
print(f"     ANY causal-public delta this estate has ever admitted, and it must do so")
print(f"     in a 2-minute window, on the instrument family where the informed-flow")
print(f"     signature was FIRST confirmed (H-FBEIA-1, wrong-signed).")

# --- Killing-constants ablation: does relaxing the cost basis rescue it? ---
# F3 freezes slip_ticks=1 as PRIMARY and slip_ticks=0 (bare commission, $1.90 RT)
# as DISCLOSURE. Using DISCLOSURE as the hurdle basis is forbidden (F3), but the
# 2026-08-10b killing-constants pattern requires showing the kill survives it.
print(f"\n--- Killing-constants ablation (does relaxing the frozen basis rescue?) ---")
ABLATIONS = {
    "PRIMARY (F3 as frozen): $0.95/side + 1 tick": 2.90,
    "DISCLOSURE basis, bare commission (FORBIDDEN as a hurdle)": 1.90,
}
for label, rt in ABLATIONS.items():
    t = COST_LAW_MULTIPLE * rt / TICK_VALUE
    bp78 = (t * TICK_VALUE / BBL_PER_CONTRACT) / 78.0 * 10_000
    print(f"  RT ${rt:.2f} -> {t:5.2f} ticks -> {bp78:5.2f} bp @ $78"
          f"  = {bp78/ceiling:.2f}x ceiling  [{label}]")
print(f"  => the kill survives the most generous admissible AND the forbidden basis;")
print(f"     it rests on the 4x multiple and MCL's tick geometry, not on the slip election.")

# --- Power limb: is it ever the binding wall, given the cost limb? ---
min_detectable_dsigma = 1.96 / (N_COMMITTED ** 0.5)
sigma_max_ticks = hurdle_ticks / min_detectable_dsigma
print(f"\n--- Power limb (PREREG F5), for completeness ---")
print(f"  min detectable delta/sigma at N={N_COMMITTED} = 1.96/sqrt(N) = {min_detectable_dsigma:.4f}")
print(f"  A delta AT the cost hurdle ({hurdle_ticks:.1f} ticks) clears power for any")
print(f"  per-event sigma <= {sigma_max_ticks:.1f} ticks (= ${sigma_max_ticks/BBL_PER_CONTRACT:.3f}/bbl).")
print(f"  A 2-minute CL window sigma is order 10-20 ticks, far below that bound, so")
print(f"  POWER IS SLACK CONDITIONAL ON COST CLEARING -- cost is the sole binding wall.")
print(f"  (The sigma magnitude is an order-of-magnitude sanity note, NOT a measurement.)")
print("=" * 74)
