# Live Requirements Audit

Use this worksheet for a specific journal, conference, workshop, publisher,
repository, or submission platform; rule-set cycle or version; paper category;
and publication stage. Populate applicable policy values from current official
sources and mark the rest `not applicable`.

## Contents

- [Official-source register](#official-source-register)
- [Requirements overlay](#requirements-overlay)
- [Artifact availability register](#artifact-availability-register)
- [Render inspection when applicable](#render-inspection-when-applicable)
- [Package inspection when applicable](#package-inspection-when-applicable)
- [Final freeze record](#final-freeze-record)

## Official-source register

| Source | URL | Version or date | Accessed | Scope | Notes or conflicts |
|---|---|---|---|---|---|
| Call for papers, author guidelines, or submission instructions | | | | | |
| Template, style guide, or form specification | | | | | |
| Policy or ethics page | | | | | |
| Supplement or artifact policy | | | | | |
| Submission platform instructions | | | | | |

## Requirements overlay

| Requirement | Exact current rule | Official source | Artifact checked | Status | Required action |
|---|---|---|---|---|---|
| Submission stage | | | | | |
| Deadline and time zone | | | | | |
| Post-deadline changes | | | | | |
| Page limit | | | | | |
| References or appendix treatment | | | | | |
| Page size and layout | | | | | |
| Fonts and spacing | | | | | |
| Figure and table rules | | | | | |
| Anonymity | | | | | |
| Author metadata | | | | | |
| Bibliography | | | | | |
| Supplement | | | | | |
| Code and data | | | | | |
| File formats and sizes | | | | | |
| Ethics and disclosures | | | | | |
| External links | | | | | |

Use `pass`, `fail`, `uncertain`, `not applicable`, or `not checked`. Do not convert uncertainty into a pass.

## Artifact availability register

| Artifact | Current access or package location | Availability status | Promised release event | Statement locations | Verified |
|---|---|---|---|---|---|

Use only `currently provided`, `included with submission`, `release upon
acceptance`, `release after publication`, or `unavailable`. Check that every
checklist response, Data Availability statement, archive README, and metadata
entry describes the same state. A future release event is not present access.

## Render inspection when applicable

Check the final artifact, not only source declarations:

- [ ] Opens in an independent viewer
- [ ] Correct page dimensions
- [ ] Correct page count
- [ ] Main content ends within the allowed section
- [ ] Fonts comply and are embedded as required
- [ ] No unresolved references or citations
- [ ] No overflow, clipping, blank pages, or broken floats
- [ ] Figures and tables remain legible at final size
- [ ] Image resolution satisfies current requirements
- [ ] Essential meaning does not rely only on color
- [ ] Metadata and links satisfy anonymity rules
- [ ] File size and format comply

## Package inspection when applicable

- [ ] Archive type and size match the live policy
- [ ] Archive extracts without errors
- [ ] Top-level structure is understandable
- [ ] No credentials, secrets, personal data, or private absolute paths
- [ ] Identity has been removed where required
- [ ] Licenses permit included redistribution
- [ ] Data are included or their permitted acquisition route is documented
- [ ] Environment and dependencies are specified
- [ ] Preprocessing, execution, and evaluation entry points are present
- [ ] Expected outputs and reproduction boundary are stated
- [ ] Manuscript statements match actual package contents

## Final freeze record

Record:

```text
governing authority or destination:
rule-set cycle or version:
paper category or track:
stage:
submission channel or delivery mechanism:
deadline and time zone, if applicable:
primary source or form revision:
primary delivered artifact hash or identifier:
supporting artifact hashes or identifiers:
last operation affecting each artifact:
audit completed:
unresolved blockers:
```

Never reuse this completed worksheet for another cycle, category, stage, or
governing authority without re-verifying every rule.
Any regeneration, recompilation, export, compression, archive rebuild, or
metadata change invalidates the checks attached to the previous hash. Freeze
and re-audit the exact upload artifact.
