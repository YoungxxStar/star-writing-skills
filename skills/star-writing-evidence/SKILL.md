---
name: star-writing-evidence
description: Design, audit, and align evidence for research and scholarly manuscripts by tracing claims to claim-specific sources, testing identification strength, checking statistical units and independence, validating metrics and constructs, challenging alternative explanations, and aligning experiments, results, figures, tables, and supplementary material. Use for claim-evidence mapping, study or experiment design, result interpretation, study-to-prose alignment, quantitative or qualitative evidence review, fairness checks, or deciding what a manuscript can defensibly claim.
---

# STAR Writing: Evidence

Treat a manuscript as a bounded, auditable argument. Determine what each source can establish before improving the prose.

## Set the audit boundary

1. Identify the manuscript snapshot, result snapshot, and requested scope.
2. Distinguish final artifacts from provisional values, plans, historical drafts, and narrative summaries.
3. Preserve read-only scope when the user asks to inspect, discuss, or audit. Do not edit files unless requested.
4. Record unavailable evidence instead of inferring or inventing it.

## Build typed provenance

Assign every material claim a type and inspect the source appropriate to that type:

- Use definitions, assumptions, and derivations for mathematical claims.
- Use executed protocols, instrument or apparatus records, code, and
  configuration for procedural or implementation claims.
- Use raw or minimally processed observations or outputs plus the analysis or
  evaluation procedure for empirical claims.
- Use original sources for claims about prior work.
- Use released artifacts, licenses, and instructions for reproducibility claims.
- Use downstream outcomes for claims of practical utility.

Do not impose a universal source hierarchy. A source is authoritative only for the kind of fact it records.

Create a ledger with:

| Field | Required content |
|---|---|
| Claim | Exact proposition, not a topic label |
| Claim type | Definition, procedural, implementation, empirical, comparative, mechanistic, generality, efficiency, utility, or reproducibility |
| Evidence | File, result, derivation, source, or artifact |
| Inference | Why the evidence supports the claim |
| Scope | Population, conditions, assumptions, and exclusions |
| Status | Supported, qualified, provisional, unsupported, or contradicted |

Read [claim-evidence-matrix.md](references/claim-evidence-matrix.md) when auditing major claims or designing missing evidence.

## Define the study contract before interpreting results

For a planned, reconstructed, or disputed experiment or analysis, read
[experiment-contract.md](references/experiment-contract.md). Record the
question, hypothesis, changed and controlled variables, independent unit,
selection rule, endpoint, metric, aggregation, uncertainty, rival explanation,
and non-conclusions before optimizing the story.

Distinguish:

- choices fixed before observing the target result;
- choices made during development or validation;
- choices made after examining final outcomes.

Do not hide post-hoc choices. A transparent exploratory analysis may be useful,
but it carries a different evidential contract from a prespecified test.

## Separate levels of inference

Keep these layers distinct:

1. **Observation** — what was directly measured, derived, or seen.
2. **Construct** — what concept the measurement is intended to represent.
3. **Inference** — what conclusion follows from the observation.
4. **Mechanism** — why the result occurred.
5. **Implication** — what future scientific or practical value may follow.

Do not present a proxy as the target construct, an interpretation as an observation, a plausible mechanism as an identified cause, or a prospective use as a demonstrated benefit.

For capability claims, audit the complete status chain:

`design permits -> configuration enables -> procedure executes -> evaluation tests -> result establishes`

Evidence for an earlier status does not establish a later one. Report the
furthest verified status and word the claim at that level.

## Match claim strength to identification

Ask what competing explanation could also produce the result. Check, as applicable:

- additional information or measurements;
- unequal data, preprocessing, or exclusions;
- unequal capacity, resources, optimization, or tuning opportunity;
- inconsistent baselines, endpoints, or post-processing;
- leakage across training, selection, and evaluation;
- case selection or aggregation choices;
- unmeasured confounding or uncontrolled environmental differences.

If the design does not distinguish the intended explanation, request a relevant control or narrow the wording. Do not attribute a whole-system comparison to an individual component without component-identifying evidence.

## Audit statistical units and independence

Identify separately:

- the unit observed;
- the unit assigned or perturbed;
- the unit that can reasonably be treated as independent;
- the unit resampled for uncertainty;
- the unit used for aggregation and reporting.

Repeated measurements from one source do not automatically create independent replicates. Check clustering, paired structure, temporal or spatial dependence, repeated measures, split leakage, missingness, and selection rules.

For every reported empirical number, recover:

- numerator, denominator, and comparison baseline;
- absolute versus relative change;
- order of aggregation;
- macro versus micro weighting;
- uncertainty definition and resampling level;
- inclusion, exclusion, and outlier rules;
- rounded display value versus calculation precision.

Then decide how the reader should encounter the number. Decompose totals whose
factors explain the study design, name the responsible manifest or protocol for
fixed counts, and omit exact values that add no interpretive or reproduction
value. A traceable number can still be a distracting magic number in prose.

Read [statistics-and-constructs.md](references/statistics-and-constructs.md) for a compact audit procedure.

## Validate constructs and metrics

For each important metric, state:

- its formula or operational definition;
- the phenomenon it directly measures;
- the broader construct it is used to represent;
- invariances and desirable direction;
- confounders and failure modes;
- what it does not establish.

Keep accuracy, sensitivity, calibration, robustness, efficiency, and causal effect distinct unless an explicit argument connects them.

## Check comparison fairness

Require parity on the dimensions necessary for the claim:

- available information;
- data and split;
- selection and tuning budget;
- training or procedural budget;
- evaluation protocol;
- post-processing;
- hardware and measurement conditions for efficiency claims.

When exact parity is impossible, document the mismatch and reduce the comparison's interpretation.

## Turn evidence into Results

Organize each result around an inferential question:

1. State the question or claim being tested.
2. Give the overall answer.
3. Report the decisive quantitative or qualitative evidence.
4. Describe heterogeneity, exceptions, and uncertainty.
5. Explain only mechanisms supported by the design.
6. State the boundary of the conclusion.

Do not narrate tables cell by cell. Recompute claims from the authoritative result source when possible; do not treat prose or captions as numerical ground truth.

## Treat visuals as evidence

Give each figure or table one primary inferential role or tightly related claim
family. For a multi-panel visual, assign every panel a subordinate role and
state how the panels combine. For every visual:

- identify the claim it supports;
- verify plotted values and caption statistics against the responsible data,
  analysis, and plotting path; do not infer them from appearance or an older
  caption;
- make units, cohorts, uncertainty, and exclusions visible;
- avoid misleading scales, selective ranges, or unmarked transformations;
- distinguish representative examples from population evidence;
- ensure the caption defines the comparison without overstating it;
- avoid encoding essential meaning through color alone.

For a result-bearing visual, require the caption to state one bounded,
source-verified observation in addition to what is shown and how to read it.
For schematics, examples, and method diagrams, state their role without forcing
an empirical conclusion. Keep detailed interpretation in the Results text when
several visuals must be synthesized.

Read
[figure-table-contract.md](references/figure-table-contract.md)
before designing a central visual, combining panels, selecting representative
examples, or changing an established figure's comparison.

## Divide main and supplementary evidence

Keep the central definitions and evidence needed to believe the main claims in the main manuscript. Use supplementary material for full derivations, implementation and protocol detail, extended diagnostics, additional cases, and secondary robustness evidence.

Do not use supplementary material as an archive, duplicate the same evidential role, or hide a central weakness outside the main argument.

## Deliver the audit

Return:

1. the claim-evidence ledger;
2. supported claims and their precise scope;
3. overclaims and unsupported inferential jumps;
4. statistical, construct, fairness, and provenance risks;
5. missing evidence ranked by its effect on the central argument;
6. defensible wording when new evidence is unavailable;
7. items not verified and why.
