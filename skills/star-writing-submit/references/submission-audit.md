# Live submission audit

Use this worksheet for a specific venue, track, year, and stage. Populate every policy value from current official sources.

## Official-source register

| Source | URL | Version or date | Accessed | Scope | Notes or conflicts |
|---|---|---|---|---|---|
| Submission instructions | | | | | |
| Author kit or template | | | | | |
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

## Render inspection

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

## Package inspection

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
venue:
track:
stage:
deadline and time zone:
manuscript source revision:
rendered manuscript hash:
supplement hash:
code/data archive hash:
last operation affecting each artifact:
audit completed:
unresolved blockers:
```

Never reuse this completed worksheet for a later year or different track without re-verifying every rule.
Any regeneration, recompilation, export, compression, archive rebuild, or
metadata change invalidates the checks attached to the previous hash. Freeze
and re-audit the exact upload artifact.
