# Skeptical scientific review rubric

Use only the sections relevant to the manuscript.

## External feedback triage

For each reviewer, collaborator, editor, or agent comment, record:

| Comment | Factual premise | Scientific risk | Evidence request | Prose preference | Policy judgment | Verification source | Verdict | Action |
|---|---|---|---|---|---|---|---|---|

Use `accept`, `partially accept`, `reject`, or `unresolved`. Judge the premise
and the proposed action separately: a comment can recommend a useful edit for
an incorrect reason, or identify a real risk while proposing the wrong remedy.

## Central argument

- Can the paper's central claim be stated as one bounded proposition?
- Is the problem scientifically meaningful without relying on promotional language?
- Does the proposed contribution answer the stated obstacle?
- Does each contribution have distinct evidence?
- Does the conclusion close the same argument opened in the introduction?

## Novelty

- What is the closest work by task and information contract, not keyword?
- Is the claimed difference substantive or only terminology, combination, scale, or implementation?
- Has the manuscript tested the strongest prior or simpler alternative?
- Does the related-work synthesis preserve meaningful differences among sources?
- Are priority claims based on an adequate and current search?

## Validity

- Are assumptions, inclusion rules, outcomes, and procedures explicit?
- Are comparisons matched on information and resources?
- Are statistical units, pairing, dependence, and aggregation correct?
- Are uncertainty and heterogeneity reported at the right level?
- Could leakage, selection, preprocessing, or tuning explain the result?
- Are equations, code behavior, prose, and figures mutually consistent?

## Mechanism

- Is the claimed mechanism observed, inferred, or hypothesized?
- Does a control or intervention isolate it?
- Could another component or contextual difference explain the same result?
- Is a qualitative pattern being used as causal evidence?
- Would the mechanism claim survive if the system-level effect remained but the named component were changed?

## Utility and significance

- Is downstream benefit measured or only plausible?
- Does the endpoint matter for the claimed use?
- Is the effect practically meaningful as well as numerically nonzero?
- Are costs, risks, and operating constraints included?
- Are novelty, validity, and usefulness evaluated separately?

## Figures and tables

- What inferential role does each visual serve?
- Can plotted values be traced to source results?
- Are scales, units, uncertainty, exclusions, and sample sizes clear?
- Are examples representative, deliberately diagnostic, or merely illustrative?
- Does the caption state conditions without making claims beyond the visual?
- Is essential information accessible without color?

## Main and supplementary material

- Can a reader assess every central claim from the main manuscript?
- Does supplementary material provide depth rather than duplication?
- Are complete derivations, protocols, extended diagnostics, and reproduction details discoverable?
- Do main and supplementary documents use the same definitions, symbols, and result versions?

## Global propagation

When one item changes, inspect:

| Changed item | Likely downstream locations |
|---|---|
| Problem definition | Title, abstract, introduction, related work, conclusion |
| Input, output, or assumption | Methods, equations, setup, captions, supplementary methods |
| Metric or aggregation | Abstract numbers, results, tables, figures, captions, limitations |
| Result value | Abstract, contributions, discussion, conclusion, supplementary summaries |
| Novelty boundary | Abstract, introduction, related work, contribution list |
| Terminology or symbol | All prose, equations, legends, captions, appendices |

## Wording-only versus evidence-required

A wording change may suffice when the evidence is sound but scope or modality is overstated. New evidence is required when the central conclusion depends on an unidentified mechanism, unfair comparison, invalid analysis, missing population, or untested utility claim.
