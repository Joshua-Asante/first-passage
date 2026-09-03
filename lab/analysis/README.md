# `lab/analysis/` — hot campaign bodies + archive stubs

**Open [`../CATALOG.md`](../CATALOG.md) In flight first.** Do not glob this
directory to infer what is live. Hot bodies means the body is still here, not
“do this next.” The operator work list is [`STATE.md`](../../STATE.md).

| Layout | Meaning |
|---|---|
| `<theme>/<slug>/` | Hot body (theme README names the family) |
| `<slug>/CARD.md` | Archived stub only; body is `lab/archive/<slug>/` — **not** a second live tree |
| `_inbox/` | Cataloged theme — unassigned until RESULTS/PREREG/Verdict; must leave before `--slug` |

Theme READMEs today: `_inbox/`, `c1/`, `harvest/`, `regime/`, `striker/`, `aegis/`,
`orb/`, `legacy/`, `mc/`.
Archive tool: `python scripts/archive_lab_analysis.py --help`.

## Phase 2 leftovers (2026-08-22)

Not a second catalog. Status / `hot` cells still flip only via
`python scripts/archive_lab_analysis.py --slug …` then `--regenerate-catalog`.
Owner for the column split: [`docs/adr/2026-08-22-catalog-hot-vs-disposition.md`](../../docs/adr/2026-08-22-catalog-hot-vs-disposition.md)
(`Accepted` 2026-08-22). This table remains the pin list (`--slug` still two-part);
CATALOG can now list a stay-hot terminal `status` with `hot=yes`.

**This pass slugged:** `dstruct_mnq_2026-08` (`NULL` — already on the RESULTS
card; Verdict stamped first so `--slug` could see it). Body:
[`lab/archive/dstruct_mnq_2026-08/`](../archive/dstruct_mnq_2026-08/).

| Hold / leave | Why `--slug` is refused or withheld |
|---|---|
| `msl_s2b_mym_2026-08` | HOLD; STAGE-1 FAIL is not archiveable |
| `cheap_falsifiers_2026-08` | HOLD; stay hot while CON-* cite them |
| `mnq_r2agrun_routeb_2026-08`, TNEC CON-2…5 | `AMBIGUOUS-HOLD` |
| `q_trainkill_{1,2,3}_2026-08` | HOLD |
| `xauusd_cgb_2026-06-15` | operational HOLD |
| `lab/analysis/time_to_pass.py` | C-P2-05; separate GO; Rule 16 inbound index first |
| `geofit_iid_sufficiency_power_2026-08-15`, `geofit_skewed_family_construction_2026-08-15` | stay-hot imports (C-P1-10) |
| `aegis_6j_prop_reconstruction_2026-07` | Wave-1 artifacts retained hot |
| `q_rail_1_2026-07` | rail evidence; many living cites |
| `msl_s4_mgc_2026-08` | PARKED; explore GO unpaid — [`README.md`](c1/msl_s4_mgc_2026-08/README.md) |
| informal ORB probes (`orbmnq1_*_probe_2026-08-20`) | C-P1-10 left ACTIVE |
| `rangestate_gc_2026-08` / `rangestate_corrected_2026-08` / `rangestate_mcl_2026-08` | family coupled; mixed SIGNAL-GENERIC |
| `ict_mnq_2026-08` | mixed W/D confirm; `cheap_falsifiers` coupling |
| `driftex_2026-08`, `eodadv_mnq_2026-08` | `**Verdict:** FALSIFIED` stamped 2026-08-23; stay-hot (frozen prereg + `rejected_candidates` + sentinel path pins); no `--slug` |
| `tnec_l2_sourcing_2026-08-10` | SCREEN-FAIL is not archiveable |
| NO_SOURCE slugs (`mnq_orb_level_proximity_tod_2026-08-06`, `mnq_sizediv_blind_2026-08`) | no RESULTS/README for `--slug` |
