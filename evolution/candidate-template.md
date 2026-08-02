# Evolution Candidate Template

Create candidate records only under the authorization and storage contract in
[README.md](README.md). Replace every instructional value below before saving a
record in `candidates/`.

```markdown
---
schema_version: 1
id: EVO-YYYYMMDDTHHMMSSZ-short-slug
record_revision: 1
created_at: YYYY-MM-DDTHH:MM:SSZ
updated_at: YYYY-MM-DDTHH:MM:SSZ
source_skill: suite
source_version: BASELINE_SEMANTIC_VERSION
baseline_revision: FULL_40_CHARACTER_GIT_COMMIT
activation: none
status: triaged
decision: investigate
scope_layer: unresolved
root_cause: instruction-gap
rule_health: not-applicable
target_owner: unresolved
review_after: none
implemented_revision: none
validated_snapshot: none
persistence_authorized: true
visibility: public-safe
privacy_review: passed
---

# Short operational title

## Episode

Summarize the user goal, observable behavior, outcome, and explicit persistence
authority without quoting raw dialogue or private artifacts.

## Diagnosis and scope

State the root cause, narrowest valid scope, responsible current rule if any,
and why this is a reusable hypothesis rather than a local fact.

## Candidate behavior

State the smallest testable behavior change. A candidate is not an active rule.

## Evidence and risk

List observable supporting evidence, counterevidence, the nearest valid
alternative, generality limits, and plausible regressions.

## Authorization boundary

State separately what is authorized for candidate persistence, active-source
changes, validation, versioning, commit, installation, push, and release.

## Validation and disposition

Record the positive case, nearest negative case, other claimed generality axes,
validation result, target owner, rollback trigger, prior validated source,
implemented commit, and adoption receipts. Use `none` for states not reached.
```

Allowed controlled values are defined in [README.md](README.md) and enforced by
`scripts/validate_plugin_suite.py`. Use `target_owner: local-layer` when the
proper destination is authorized author, project, or submission state. Use a
repository-relative file path only after a canonical active-rule owner is
identified; the baseline revision preserves the historical meaning if that
owner later moves.
