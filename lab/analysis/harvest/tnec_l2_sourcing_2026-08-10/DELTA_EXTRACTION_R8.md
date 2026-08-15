# R8 δ-extraction — gold PM-fix window (Caminschi–Heaney *JFM* 2014) → `SCREEN-FAIL`

**Date:** 2026-08-10 (operator GO in-session) · **$0 · K=0 · no manifest opened · no market data pulled**
**Source retrieved:** UWA green-OA accepted manuscript, `api.research-repository.uwa.edu.au/ws/files/4725264/A0205_use_this.pdf`
(1,077,264 bytes, `%PDF` verified; Unpaywall/OpenAlex both list it as the sole OA location for DOI `10.1002/fut.21636`).
49 pp, full text extracted locally. ⚠ The web-front copies (repository page, doczz) are Cloudflare-challenged — the Pure
API host is the reproducible route.

## What the paper measures (GC futures cohort, 2007-01-01 → 2012-12-31, n≈1,470 fix-days; 1m bars)

Verbatim decomposition (§ around Table 6; "adjusted" = signed by the **eventual fix direction**, known only to
fixing participants pre-publication):

> "the initial four minutes (1 ≤ i ≤ 4) showing the difference in returns of **+3.8 bps, +3.0 bps, +1.8 bps and
> +1.0 bps** for GC … t-test statistics … from over **+17** … down to **+7.2**"
> "the unadjusted returns in the first two minutes … are smaller … **UR+1 = −0.6 bps (t −3.3)**, **UR+2 = −1.2 bps
> (t −6.7)** … The subsequent two minutes (i = 3, 4) show **no significant unadjusted returns**"
> "**We find no significant impacts or returns following the publication of the fixing results.**"
> Abstract: "return advantages in the four minutes following the start of the fixing **for informed traders**";
> summary: "~9 bps in the four minutes … and a possible further 4 bps in the two minutes before the **end** of the
> fixing" (fix end time is participant-known, not public, pre-reform; median duration ~10 min, Table 2).

Table 8 (the leakage): sign of the public GC move from fix start predicts the fix direction — 73.6% at the 15:02
cut-off (all fixes, n=329), 86.7% on the big-fix half (n=165), rising toward ~94% later as n shrinks.

## Admissibility split (the load-bearing step)

- **The headline δ (~9.6 + ~4 bp) is Req-2-INADMISSIBLE**: it attaches to fix-direction knowledge before
  publication — the informed-flow class (`H-FBEIA-1` CL-EIA is the worked precedent; NG-EIA-1's pre-leg the
  second). **Third confirmed instance of the signature**: large real event-reaction, near-zero unconditional
  public edge (UR+1/UR+2 total ≈ −1.8 bp and wrong-shaped; i=3,4 unadjusted n.s.).
- **The causal public expression** (enter at 15:02 with the sign of the public 2-minute move — Table 8's MKTDIR)
  captures only the *residual* adjusted drift after the leak has moved the price: i=3,4 (+2.8 bp) plus, only if
  the fix-end could be timed (it cannot, publicly, pre-reform), the ~4 bp end-block.

## Req-5 sniff (executed arithmetic; RT = 2 ticks + 2 × $1.06 Metals cps)

| Expression | cost_bp | 4× hurdle | Causal δ bound (2P−1)×remaining | Verdict |
|---|---|---|---|---|
| MGC @ $1,600 (paper's basis) | 2.575 | **10.30 bp** | 1.32–3.21 bp (all fixes) | **KILL, 3.2–7.8× under** |
| MGC @ $2,600 (modern) | 1.585 | **6.34 bp** | 1.32–3.21 bp | **KILL, 2.0–4.8× under** |
| GC @ $2,600 (best legal case) | 0.851 | **3.40 bp** | 3.21 bp generous top (incl. untimeable end-block) | **KILL — under even at the indefensible top** |
| GC big-fix-half only | — | 3.40 bp | 2.06–4.99 bp | selection on the conditioning half is a K-charge; and the 4.99 top needs the untimeable end-block — not a rescue |

Every venue-legal expression fails **before** the mandatory post-2015 decay haircut. The reform direction is
adverse by published evidence: *JFM* 2020 (`10.1002/fut.22120`) finds the auction reform narrowed spreads and
deepened books — the leakage channel the pre-reform δ rode was structurally reduced. The paper's own 3 bp
"economic" threshold was for the **informed** 9.6 bp at GC parent costs, not for the public residue.

## Verdict

**`SCREEN-FAIL (informed-flow + Req-5 cost-law)` — on the seed's own mechanism record**, replacing the void
2026-07 Req-3 K-kill. The R8 re-stage did exactly what it was for: the seed now stands-or-falls on merits, and
it falls. Family scope: any benchmark-fix-window construct on the venue-legal metals set (GC/MGC/SI/SIL) inherits
this arithmetic — silver's cost_bp is worse and its fix literature reports the same informed structure.
**Re-proposal bar:** a *post-reform, publicly-conditioned* cohort δ ≥ the 4× hurdle at a named venue-legal
expression — not a re-read of pre-reform tables, not the informed-side numbers, not a window re-tune.

**K accounting:** no PnL computed on our data; published-table arithmetic only. `discovery_manifests/` unchanged.
