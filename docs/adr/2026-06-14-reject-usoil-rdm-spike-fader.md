# 2026-06-14 — Reject short-only mean-reversion spike-fader on USOIL (edge-failure)

**Status:** `Accepted` — REJECT (edge-failure + venue/cost-constraint). The kill is **confirmed on the canonical `PEPPERSTONE:SPOTCRUDE` feed** (the load-bearing reproduction the `Proposed` draft was waiting on). All three pre-registered limbs falsified.
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Decision date:** 2026-06-14
**Authors:** Joshua + claude.ai (advisor, web session) → reconciled + canonically reproduced by Claude Code
**Concept ID:** `CONCEPT-USOIL-RDM-001` (working name: short-only Aegis-style spike-fader, USOIL). *ID disambiguation: "RDM" here = reversion/mean-reversion-fader; NOT the USDCAD `CONCEPT-USDCAD-RDM-001` "Sovereign rate-differential" mechanism.*
**Rejection class:** `edge-failure` (primary) + `venue/cost-constraint` (secondary).
**Related:** [`2026-06-14-rejected-candidate-patterns.md`](2026-06-14-rejected-candidate-patterns.md) (the taxonomy this is classified under — worked exemplar) · [`2026-06-12-tv-csv-canonical-feed-policy.md`](2026-06-12-tv-csv-canonical-feed-policy.md) · [`ops/instruments/USOIL.md`](../../ops/instruments/USOIL.md) (instrument ledger, D3)
**Layer:** portfolio (R&D corpus)

> **Provenance (Rule 0).** Authored in a web session (no repo access) against the non-canonical `FX_USOIL` 4H feed. Reconciled to the repo and then **reproduced on the canonical `PEPPERSTONE:SPOTCRUDE` panel** (the deployment feed). The canonical run kills the concept *harder* than the staging run — gross expectancy is negative at every target cell on the clean feed. Full results: [`lab/archive/usoil_rdm/RESULTS.md`](../../lab/archive/usoil_rdm/RESULTS.md).

---

## §0 — Rule 0 reads (production / analysis-of-record before authoring)

**Repo reads:**
- [`ops/instruments/USOIL.md`](../../ops/instruments/USOIL.md) — anchor `4e50deb` (verified `git log -1` on 2026-06-14). Operational rule 10 mandates this read. **Canonical panel = `PEPPERSTONE:SPOTCRUDE` 15m, 2020-01-01→2023-12-29** (SHA `256780f0…`); `TVC:USOIL`/`FX_USOIL`-class symbols are corruption-bearing (W1/F1). F4: ATR% feed-stable (3.06≈3.07).
- [`docs/adr/2026-06-12-tv-csv-canonical-feed-policy.md`](2026-06-12-tv-csv-canonical-feed-policy.md) — anchor `6f8063a`. TV-export/deployment feed is canonical; other symbols are staging-only.
- `lab/validation/concept_intake/concepts/` — no `CONCEPT-USOIL-RDM-001.yaml` → the concept never passed the intake gate; no harness `DispositionRecord`. The registry entry (§7) is hand-authored under the companion ADR §D schema.

**Analysis-of-record (now IN-REPO under `lab/analysis/usoil_rdm/`):**
- [`probe4h.py`](../../lab/archive/usoil_rdm/probe4h.py) + [`probe4h_run_FXUSOIL_staging.log`](../../lab/analysis/usoil_rdm/probe4h_run_FXUSOIL_staging.log) — the web-session staging probe; reproduces the original numbers exactly (bar-walk first-touch, amb=0 all cells).
- [`probe4h_canonical.py`](../../lab/archive/usoil_rdm/probe4h_canonical.py) + [`probe4h_run_canonical_c35c1.log`](../../lab/analysis/usoil_rdm/probe4h_run_canonical_c35c1.log) — the canonical port (15m→4H resample, same engine).
- [`costlaw.py`](../../lab/archive/usoil_rdm/costlaw.py) — assumed-stop cost-law table.
- [`RESULTS.md`](../../lab/archive/usoil_rdm/RESULTS.md) — verdict + both-feed comparison.
- Raw panels (`FX_USOIL` staging CSV, `PEPPERSTONE:SPOTCRUDE` `c35c1`) are vendor data (gitignored class) — not committed; the canonical SHA/source is pinned in the ledger.

---

## §1 — Context

`CONCEPT-USOIL-RDM-001` emerged from the government-intervention arc: upside spikes not backed by a persistent physical supply loss tend to revert, suggesting a short-only fader (anchor SMA50/4H; overext `close > anchor + 2·ATR14`; entry = first close back inside the envelope; stop = spike high; shallow T·ATR target). The web session gated it through a cost-law pre-flight (passed *conditional on* execution TF ≥ 4H), a daily proxy probe (marginal, p≈0.10), then a pre-registered 4H "decisive" probe. The probe killed it — but ran on `FX_USOIL`, a feed the repo de-canonicalized for this instrument. This ADR records the canonical reproduction.

**Decision driver (one sentence):** the cheapest correct kill (cost-geometry from the realized stop) was already decisive, and the canonical re-run confirms it on the feed Joshua actually trades.

---

## §2 — Decision

**Decision:** Reject `CONCEPT-USOIL-RDM-001` as **edge-failure + venue/cost-constraint**. Killed pre-build (0 forward slots). The rejection rests on the feed-robust **cost-geometry limb**, with placebo + stationarity corroborating on **both** the staging and canonical feeds.

**Effective:** immediately on acceptance. Registry entry written (companion ADR §D schema); USOIL ledger D3 appended.
**Scope:** the short-only mean-reversion spike-fade mechanism (`role_tested=entry`) on USOIL only. Distinct mechanism class from D1 (Guardian trend transplant), D2 (carry / CONCEPT-USOIL-CARRY-001), and the active `CONCEPT-USOIL-RGC-001` (breakout regime-capture) — not a rediscovery (composite key `mean-reversion-spike-fade × USOIL` is new).

---

## §3 — Evidence (canonical primary; staging corroborating)

Bar-walk first-touch resolution; only same-bar double-touch is ambiguous (amb ≈ 0). Full table in [`RESULTS.md`](../../lab/archive/usoil_rdm/RESULTS.md).

### Canonical `PEPPERSTONE:SPOTCRUDE` (4H, 2020-01-01..2023-12-29, n=198 @ m2.0) — **load-bearing**

| Limb | Result | Reading |
|---|---|---|
| **(b) Cost geometry** | mean realized cost **0.090R**; net E[R] −0.113/−0.167/−0.181/−0.213 at T=1.0/1.5/2.0/2.5 → **gross negative at every cell** (best T=1.0 = −0.023 gross) | No gross edge before cost; sub-ATR stop infeasible. |
| **(a) Placebo** (m2.0,H30,T1.5) | real −0.167 vs random-day null −0.110 (sd 0.098), **p=0.718** | Indistinguishable from a random short. |
| **(c) Stationarity** (thirds) | −0.069 / −0.274 / −0.115 — **all negative** | No positive regime in the canonical window. |
| Kill-switch | −0.167 → −0.164 | Cannot manufacture an edge. |
| Horizon (H=12/30/60) | −0.147 / −0.167 / −0.141 | Negative everywhere. |

Robust to the COVID window: `--excl-apr` gives net −0.150 @ T=1.5, placebo p=0.664.

### Staging `FX_USOIL` (4H, 2020-2026, n=309 @ m2.0) — corroborating

Mean cost 0.081R; least-bad cell T=2.0 net −0.044 (gross ≈ +0.037, thin); placebo p=0.273; thirds −0.149/−0.067/**+0.008** (recent third statistically zero, n=102, SE ±0.10). The +0.008 outlier is the *only* non-negative cell across both feeds and does not survive on canonical.

**Why the daily proxy looked marginally positive (superseded):** an unresolved ambiguous bucket scored at the random-path midpoint, a proxy feed (CL=F), and a generic 0.03R cost vs the realized ~0.09R. The cost correction is load-bearing — the L-COST-GEOMETRY firing (companion ADR §lessons): the *assumed* k·ATR pre-flight reads "comfortable" at 4H, the *realized* spike-to-reentry stop is sub-ATR → ~0.09R.

---

## §4 — Falsifiable hypothesis (pre-registered; resolved)

**Hypothesis (H, pre-registered):**

> **If** the fader's net expectancy on the canonical panel (a) beats a matched random-day placebo (p<0.05), **and** (b) clears the cost hurdle with margin, **and** (c) is stationary across panel thirds — **then** admissible to a Pine build + forward slot; **otherwise** reject as edge-failure (re-openable only on a NEW mechanism, not a re-tune).

**Resolution: FALSIFIED on all three limbs, on the canonical feed.** (a) p=0.718; (b) gross expectancy negative at every cell before cost; (c) all canonical thirds negative. The staging feed corroborates (the lone +0.008 recent third is statistically zero and absent on canonical). The 2024–26 period is outside the canonical panel; the staging feed covers it and shows no edge there either.

---

## §5 — Forbidden moves (genuinely tempting this session)

- **(a) Re-tune to a passing config.** Search anchor/m/target/horizon until a positive cell appears — selection-hacking; a plateau around a spurious selection still passes.
- **(b) Promote the staging +0.008 recent third as a regime edge.** Subset-significance trap (n=102, SE ±0.10, statistically zero); absent on canonical; "works only lately, no mechanism" is the path-overfit residual.
- **(c) Widen the stop post-hoc to cut cost.** Design-layer `p`-hacking; gross is negative even before cost on canonical, and a wider stop reshapes win/loss geometry.
- **(d) Cite the `FX_USOIL` numbers as canonical.** The repo de-canonicalized that symbol for USOIL (W1/F1); the canonical reproduction is what carries the rejection.
- **(e) Lean on the kill-switch to rescue expectancy.** Protection only; demonstrated unable to flip net-negative to positive (−0.167 → −0.164).

---

## §6 — Gate (binary)

**Verdict: REJECT — edge-failure; the §4 hypothesis is FALSIFIED on all three limbs on the canonical `PEPPERSTONE:SPOTCRUDE` feed. Status `Accepted`.** Triggers met: placebo p=0.718 (≥0.05), net E[R] negative at all T and all H, gross negative at every cell, thirds all negative.

**Add-back condition (companion ADR §A, edge-failure class):** re-admissible **only** on a *genuinely new entry mechanism* (distinct class). NOT: a parameter re-tune of this fade logic; a new subset/regime slice; a stop-geometry change to this confirmation entry. Per role-asymmetry (`role_tested=entry`), a fade *signal* could still be probed as an exit/filter without clearing this entry-rejection bar.

---

## §7 — Implementation plan (executed)

- **Phase 0** ✅ — read `ops/instruments/USOIL.md` (rule 10); canonical panel SHA confirmed (`256780f0…`).
- **Phase 1** ✅ — probe + costlaw + logs committed under `lab/analysis/usoil_rdm/` (the `lab/analysis/` mechanism-probe lane, NOT the confabulated `scripts/research/usoil_rdm/`). Staging run reproduced exactly.
- **Phase 2** ✅ — limb (b) reproduced on `PEPPERSTONE:SPOTCRUDE` (mean cost 0.090R; gross negative at every cell). **Load-bearing reproduction passed.**
- **Phase 3** ✅ — limbs (a)+(c) reproduced on canonical (p=0.718; all thirds negative). Coverage gap noted: canonical panel ends 2023-12-29; 2024–26 covered only by staging (also no edge).
- **Phase 4** ✅ — concept has no intake YAML; registry entry hand-authored under companion ADR §D schema (`class/role_tested/falsifier_failed/addback_condition/config_fingerprint`).
- **Phase 5** ✅ — `docs/rejected_candidates.md` entry appended; `ops/instruments/USOIL.md` D3 + session log + changelog appended.

---

## §10 — Audit hooks (runnable)

```bash
# 1. No Pine build / forward slot for this concept (must return nothing)
grep -rl "USOIL-RDM\|usoil_rdm" --include=*.pine . 2>/dev/null
grep -rin "USOIL-RDM" docs/briefs/ docs/briefs/pre-registration/ 2>/dev/null

# 2. Registry entry exists and is classed edge-failure
grep -n "mean-reversion-spike-fade\|USOIL-RDM" docs/rejected_candidates.md

# 3. Kill reproduces on canonical (expect mean cost ~0.090, net E[R]<0, placebo p>=0.5)
python lab/archive/usoil_rdm/probe4h_canonical.py <PEPPERSTONE_SPOTCRUDE_c35c1.csv>

# 4. Dedup catches a rediscovery of this direction
python -c "from lab.validation.concept_intake.dedup import load_registry; \
print([ (x.mechanism_family,x.instrument) for x in load_registry() if x.instrument=='USOIL'])"

# 5. Probe lane in-repo
test -d lab/analysis/usoil_rdm && echo "probe in-repo" || echo "MISSING"
```

---

## Verification

```bash
python scripts/check_brief.py docs/adr/2026-06-14-reject-usoil-rdm-spike-fader.md --type adr
# Expected: all 6 checks PASS
git log -1 -- ops/instruments/USOIL.md
python lab/archive/usoil_rdm/probe4h.py            # staging reproduces web run
python lab/archive/usoil_rdm/probe4h_canonical.py <c35c1.csv>   # canonical kill
ls lab/validation/concept_intake/concepts/ | grep -i "usoil-rdm" || echo "no RDM yaml (expected — never intaked)"
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-06-14 | Initial authoring (web session) — `FX_USOIL` 4H, claimed "canonical", confab paths | Joshua + claude.ai |
| 2026-06-14 | Reconciled to repo: `Proposed` (REJECT-PENDING-CANONICAL); paths fixed; intake-gap + ID-collision flagged | Claude Code |
| 2026-06-14 | **Canonically reproduced** on `PEPPERSTONE:SPOTCRUDE` (mean cost 0.090R, gross neg every cell, placebo p=0.718, all thirds neg) → status `Accepted`; artifacts in-repo; registry + ledger D3 written | Claude Code |
