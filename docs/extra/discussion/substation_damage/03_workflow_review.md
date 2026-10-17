<!--
author: owner-directed (Divy) · agent-researched
created: 2026-10-16
updated: 2026-10-16
status: active
scope: Concrete repository and skill findings from the first substation reuse exercise.
-->

# Damage workflow review — improve the handoffs

Damage has substantial methodology, provenance, schemas and release rules. Its weaker point in this
exercise is how a reader moves between them and identifies what remains unproved. We used the existing
structure; no repository reorganization or replacement framework was needed.

| Finding | Evidence/impact | Action and owner |
|---|---|---|
| Existing reuse discipline is useful | Standard 20 and the Flood-electrical substrate already separate shared evidence from runtime reuse | Reuse those rules; no universal component loader before two qualified cells and contract migration |
| A reproducible curve can be mistaken for a qualified new profile | Same table passes 93 cases while geometry and repair scope remain unresolved | Added one progress table/receipt convention to intake guide and worksheet; exercised in this package |
| Fresh source retrieval can be confused with prior verification | FEMA 403, but exact governed source pins/table already exist | Separate inherited/fresh evidence and record the specific outstanding claim; preserve prior research |
| Tail guidance is inconsistent | New-cell workflow said tails require spread; reportability rules already require an annual loss distribution | Skill 0.8 aligns the workflow/capability guide with the existing ownership boundary; deterministic DR can feed annual hazard variation |
| Reference evaluator carries historical proposal metadata | `flood_wind_curve_eval.py:494` hardcodes proposal scenario status | Recorded; no silent canonical helper change. Production consumer admission must be proved when implemented |
| Canonical status differs from portable packaging and notebook readiness | Current cell releases exist; separate notebook coverage plan documents broken/stale reader paths | Link the prior plan; this task will create an executed reader after its model exists, without claiming repo-wide repair |
| Generic skill capability example differs from live v3 representation | The guide illustrates concepts; current JSON/schema has its own required fields | Clarified authority; actual schema migration remains a separately classified task |

## Change classification and version consequence

This work is research/evidence and documentation outside current cell packages, plus a **SKILL_REVISION
0.7 → 0.8**. No curve form, parameter, runtime selector/conditioner, runtime value mapping, artifact,
capability, schema, package index or consumer pin changes. Existing cell model/docs revisions stay fixed
because their governed packages were not edited. The next standalone candidate is a new-cell or explicit
binding change under the existing workflow, not something implied by this review.

The skill's docs/evidence workflow requires a docs-revision bump when a cell's governed proof package is
changed. That does not require a cell bump for this separate pre-cell discussion or skill revision.

## Validation and scope

The concrete application is the [93-case and value review](verification/README.md). Skill checks are
recorded in its [validation report](../../damage_curve_skill/VALIDATION_REPORT.md). Existing governance
self-tests check the classifier; they do not prove research judgment or standalone response applicability.
Manual walkthroughs cover the elevation mismatch, whole-assembly denominator, stale helper metadata,
annual-withholding gate, and continuing source research without discarding inherited evidence.

User-facing numerical release and any broader architecture work remain future work. This checkpoint is
useful because another researcher can reproduce exactly what passed and identify who owns what remains.
