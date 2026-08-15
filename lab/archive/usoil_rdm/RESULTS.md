# CONCEPT-USOIL-RDM-001 — spike-fader kill: results (staging + canonical)

**Verdict: REJECT — edge-failure (+ venue/cost-constraint).** Falsified on all three
pre-registered limbs, **confirmed on the canonical `PEPPERSTONE:SPOTCRUDE` feed**.
ADR: [`docs/adr/2026-06-14-reject-usoil-rdm-spike-fader.md`](lab/archive/../../docs/adr/2026-06-14-reject-usoil-rdm-spike-fader.md).

Mechanism tested: short-only mean-reversion fade of upside overextension. Anchor
SMA50 (4H); overextension `close > anchor + 2·ATR14`; entry = first close back
inside the envelope; **stop = spike high**; shallow reversion target (T·ATR).
Role tested: **ENTRY** signal only (not exit/filter/size).

## Panels

| Feed | Symbol | TF | Range | Bars | Note |
|---|---|---|---|---|---|
| **Staging** | `FX_USOIL` | 4H native | 2020-01-02 .. 2026-06-11 | 9,763 (Apr-2020 + sub-$1 excised, 186 removed) | Non-canonical, **corruption-bearing** (sub-$1 April-2020 prints = same negative-WTI artifact that retired `TVC:USOIL`). |
| **Canonical** | `PEPPERSTONE:SPOTCRUDE` (`c35c1`, SHA `256780f0…`) | 15m → resampled 4H (epoch-aligned UTC) | 2020-01-01 .. 2023-12-29 | 6,395 4H (clean; 0 sub-$5; $9.85–$131.82) | The deployment feed (per [`ops/instruments/USOIL.md`](lab/archive/../../ops/instruments/USOIL.md), 2026-06-12 TV-CSV-canonical ADR). **Does not cover 2024–26.** |

Step-0 (canonical): median native spacing 900s (15m confirmed); resampled 4H bars
land on `[0,4,8,12,16,20]` UTC boundaries; 0 sub-$5 bars; no Apr-2020 corruption
(Pepperstone tracked the June contract). `--excl-apr` robustness run included.

## Three-limb resolution

| Limb | Staging (`FX_USOIL`) | Canonical (`PEPPERSTONE:SPOTCRUDE`) | Verdict |
|---|---|---|---|
| **(b) Cost geometry** | mean cost **0.081R**; least-bad cell T=2.0 net −0.044 → gross ≈ **+0.037R** (thin) | mean cost **0.090R**; **gross negative at ALL cells** (best T=1.0: net −0.113 + 0.090 = **−0.023 gross**) | **FALSIFIED** (feed-robust; worse on canonical) |
| **(a) Placebo** (m2.0,H30,T1.5) | real −0.072 vs null −0.114, **p=0.273** | real −0.167 vs null −0.110, **p=0.718** | **FALSIFIED** (no edge over random short; clearer on canonical) |
| **(c) Stationarity** (thirds, net mid) | −0.149 / −0.067 / **+0.008** (recent third statistically zero, n=102) | −0.069 / −0.274 / −0.115 (**all negative**; window = 2020-23 only) | **FALSIFIED** (no positive regime in the canonical window) |

Supporting (canonical): kill-switch −0.167 → −0.164 (cannot manufacture an edge);
horizon −0.147 / −0.167 / −0.141 at H=12/30/60 (negative everywhere).

## The cost-law lesson (L-COST-GEOMETRY, worked)

`costlaw.py` computes the **assumed** k·ATR pre-flight: 4H @ k=2.5, x=0.08 →
`Cost_R = 0.08/(2.5·3.00) = 0.011R` ("comfortable"). But the **realized** stop is
`spike_high − entry` (a confirmation re-entry just below the high) ≈ **sub-ATR**
(~$0.9 at 4H), so the realized hurdle is `0.08/0.9 ≈ 0.09R` — ~8× the assumed
figure, and above the (negative) gross edge. A "confirmation entry + stop above
the spike high" fader is structurally sub-ATR-stopped → cost-infeasible regardless
of feed. This is the L-COST-GEOMETRY firing recorded in
[`docs/adr/2026-06-14-rejected-candidate-patterns.md`](lab/archive/../../docs/adr/2026-06-14-rejected-candidate-patterns.md) §lessons.

## Reproduce

```bash
# Staging (FX_USOIL) — reproduces the web-session run exactly:
python probe4h.py
# Canonical (PEPPERSTONE:SPOTCRUDE) — the load-bearing reproduction:
python probe4h_canonical.py /path/to/BAR_EXPORT_v0.1_PEPPERSTONE_SPOTCRUDE_2026-06-13_c35c1.csv
python probe4h_canonical.py <panel.csv> --excl-apr   # COVID-window robustness
python costlaw.py                                     # assumed-stop cost bands
# Expected (canonical): mean cost ~0.090R, net E[R]<0 all T, placebo p>=0.5, all thirds <0.
```

Logs: `probe4h_run_FXUSOIL_staging.log` (staging), `probe4h_run_canonical_c35c1.log`
(canonical). Raw panels are vendor data (gitignored class — not committed); the
canonical panel's SHA/source is pinned in the USOIL ledger.

## Add-back condition

Re-admissible **only** on a genuinely new entry mechanism (distinct class) — NOT a
re-tune, subset/regime slice, or stop-geometry tweak of this confirmation-fade
entry. `role_tested=entry`: a fade *signal* could still be probed as an exit/filter
without clearing this bar (role-asymmetry).
