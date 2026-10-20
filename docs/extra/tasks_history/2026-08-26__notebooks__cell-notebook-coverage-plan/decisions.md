# Decisions — cell notebook coverage plan session (2026-08-26)

The plan's own register is `docs/plans/cell_notebook_coverage/decisions.md` (NB-D01…D10). These are the
session-level choices about *how the documentation was laid down*.

## 1. Write a plan, not the notebooks

**Decision:** deliver a plan of record, contract, per-cell packages and registers; do not build or repair any
notebook in this session.

**Rationale:** the owner asked for a detailed plan. Repairing the two broken pairs is Phase 0 of that plan and
is the first thing to execute once gate G1 is answered.

## 2. Station 1 before station 2

**Decision:** write a discussion node (`docs/extra/discussion/cell_notebook_coverage/`) before the plan, even
though the direction was owner-stated.

**Rationale:** the Hazard workflow allows skipping a station but not silently; the node records the
verification (what was actually on disk / in git / on the remote), the options rejected and the pressure
tests, which the plan then references instead of repeating.

## 3. Mirror Hazard's conventions without rewriting other people's docs

**Decision:** add the 5-field stamp, ledger columns and templates; for pre-existing plan/discussion rows,
fill `Date` from the folder's first git commit and `Created by` from the git author, and keep each row's
recorded status phrase verbatim rather than mapping it onto the closed vocabulary.

**Rationale:** the stamp is the authority and the table is an index over it. The legacy docs have no stamp,
so inventing a closed-vocabulary status for them would put a claim in the index that no document supports.
They are backfilled opportunistically when each doc gets its stamp.

## 4. Fix the stale path in READMEs, leave the notebooks' cells alone

**Decision:** correct `docs/damage_curves/…` → `docs/cells/…` in `notebooks/README.md` and the two per-asset
READMEs, and add an explicit "broken until Phase 0" notice; do not edit `.ipynb` files.

**Rationale:** a README pointing at a removed path is a stale current representation and is cheap to fix;
editing notebook cells without re-executing and reconciling prose to the r7/r4 artifacts would be a
half-repair that looks finished.

## 5. Templates live tier-local

**Decision:** `docs/plans/_templates/` and `docs/extra/discussion/_templates/`, not `docs/method/templates/`.

**Rationale:** `docs/method/templates/` holds cell-package templates (the curve discipline); plan and
discussion templates belong beside the folders they govern, which is the Hazard rule ("conventions stay
local, next to the files they govern") and what the owner asked to bring over.

## 6. Do not touch the CI claim in `AGENTS.md`

**Decision:** leave the `.github/workflows/` "CI (starter)" row alone; record the stale claim here.

**Rationale:** the 2026-08-18 review already flagged it and it is outside this task; the plan's NB-D10 makes
headless execution a manual gate precisely because CI does not exist.
