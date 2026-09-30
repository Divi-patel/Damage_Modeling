# Release decision — tropical-cyclone wind × solar model v2.1 / docs r2

```yaml
decision_date: 2026-08-30
decision: promote_as_canonical_coverage_complete_screening_model
runtime_schema: damage_curve_record_bundle.v3
portable_package: unchanged_at_library_v2.5
headline_scenario: central_screening
```

The owner accepted the labeled screening-grade method after the Everglades observed-asset experiment used
the exact proposed artifact and passed all 18 predeclared M0→M4 checks. The accepted production policy is:

- use `central_screening` as the headline, not as certainty;
- retain lower- and upper-resistance alternatives in the immutable run evidence;
- admit labeled Tier-P modeled spatial support when observed support is unavailable;
- make no O1 platform-database schema change for this Damage release;
- permit downstream Hazard EAL/PML only after exact pin, frequency/coupling, cap and value validation.

Promotion changes the canonical identity, paths and release metadata. It does not change curve records,
parameters, value composition, scenario arithmetic or screening outputs. A dedicated validator compares both
artifacts across fixed and tracker demand grids and requires the current KAT fixture to differ only by the
canonical identity and status metadata.

Docs r2 is the fix-forward current release. The immutable docs-r1 publication preserved correct numerical
outputs but inherited `NONCANONICAL_MODEL_V2_1` in its KAT metadata. Docs r2 replaces that stale label with
`CANONICAL_SCREENING_RELEASE`; all curve records, supporting machine bytes and numerical results remain
unchanged. Docs r1 is retained as immutable history and must be marked superseded by the consumer registry.

This decision does not claim calibration, bankability, probabilistic uncertainty, rain/debris/surge coverage,
or a general hurricane-loss model. Better evidence should replace Tier-4 curves in a later semantic model
version; it does not invalidate this explicitly labeled screening release.
