---
name: star-writing-evidence
description: Design, audit, and align evidence for research papers by tracing claims to claim-specific sources, testing identification strength, checking units and dependence, validating measures and constructs, challenging alternatives, and aligning studies, analyses, results, and visuals. Use for claim-evidence mapping, study design, result interpretation, quantitative or qualitative review, comparison fairness, or deciding what a paper can defensibly establish across fields and projects.
---

# STAR Writing: Evidence

Treat a manuscript as a bounded, auditable argument. Determine what each source can establish before improving the prose.

Do not load the
[evolution handoff overlay](../star-writing/references/evolution-policy.md) for
ordinary paper work. If the user explicitly requests reusable learning, keep
this skill responsible for the paper and return only a public-safe task-local
handoff. Do not persist learning state or change skill source.

## Set the mode

- Use **audit** by default to inspect evidence, results, metrics, statistics,
  visuals, or claim support without modifying source artifacts.
- Use **plan** to design an experiment, analysis, metric, evidence package, or
  visual contract. Mark planned evidence as unevaluated until it is executed and
  verified.
- Evidence work may recommend defensible wording, but manuscript drafting or
  file revision remains with `star-writing-draft` unless separately authorized.

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

Create a task-local claim-evidence ledger with:

| Field | Required content |
|---|---|
| Claim | Exact proposition, not a topic label |
| Claim type | Definition, procedural, implementation, empirical, comparative, mechanistic, generality, efficiency, utility, or reproducibility |
| Evidence | File, result, derivation, source, or artifact |
| Inference | Why the evidence supports the claim |
| Scope | Population, conditions, assumptions, and exclusions |
| Claim status | Established, bounded, exploratory, unsupported, contradicted, or unresolved |

Keep this ledger in the current task unless the user authorizes a persistent
artifact and its location. It is not a second source of truth; its entries point
to the responsible evidence. This claim-evidence ledger is an analysis view,
not the Project Writing Ledger, and it does not own canonical semantic entries.

Before substantive work, follow
[the Writing Ledger contract](../star-writing/references/writing-ledger-contract.md).
Load only the relevant accepted metric, condition, population, baseline,
result, concept, and symbol entries; do not create stylistic aliases. Evidence
work determines support and claim status and may report an entry task-locally
as stale, but `star-writing-ledger` owns persistent semantic decisions.

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
furthest established stage and word the claim at that level.

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

Apply this standard symmetrically. Search for disconfirming evidence and rival
explanations, but do not treat every conceivable rival as equally plausible.
When the design excludes a rival, say so and retain the strongest supported
conclusion. Missing evidence leaves an issue unresolved; it does not by itself
make the claim false.

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

## Allocate evidence when supporting material exists

Keep the central definitions and evidence needed to assess the main claims in
the paper. When the target permits supporting material, use it for full
derivations, implementation and protocol detail, extended diagnostics,
additional cases, and secondary robustness evidence.

Do not invent supporting material, use it as an archive, duplicate the same
evidential role, or hide a central weakness outside the paper's argument.

## Deliver the audit

Return:

1. the claim-evidence ledger;
2. supported claims and their precise scope;
3. overclaims and unsupported inferential jumps;
4. statistical, construct, fairness, and provenance risks;
5. missing evidence ranked by its effect on the central argument;
6. defensible wording when new evidence is unavailable;
7. items not verified and why.

Label each substantive wording recommendation with
[one highlighted governing principle](../star-writing/references/principle-tags.md),
then state its evidence and boundary separately. Keep tags outside the target
artifact and do not use them as support for a claim.
