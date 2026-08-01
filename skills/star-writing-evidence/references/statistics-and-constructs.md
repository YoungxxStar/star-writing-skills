# Statistical and construct audit

## Statistical unit worksheet

Record:

| Question | Answer |
|---|---|
| What is observed? | |
| What is assigned, selected, or perturbed? | |
| What is the independent unit? | |
| What creates dependence or clustering? | |
| What unit is resampled for uncertainty? | |
| What unit is averaged first? | |
| What population does the estimate target? | |

Flag pseudoreplication when the reported sample count is larger than the number of independent units without an appropriate hierarchical or dependence-aware analysis.

## Aggregation reconstruction

Recover the calculation in this order:

1. Define the eligible observations.
2. Define any within-unit summary.
3. Define pairing or matching.
4. Define group or stratum summaries.
5. Define weighting across groups.
6. Define the final estimator.
7. Define uncertainty at the correct resampling level.
8. Verify that displayed rounding did not drive the calculation.

State whether a change is:

```text
absolute change = new - reference
relative change = (new - reference) / reference
relative reduction = (reference - new) / reference
```

Name the denominator whenever reporting a percentage.

## Construct-validity worksheet

For each metric:

| Question | Answer |
|---|---|
| What is computed directly? | |
| What construct is inferred? | |
| Why should the metric track that construct? | |
| What else can change the metric? | |
| What does a high or low value not imply? | |
| Is the direction comparable across settings? | |
| Are there floor, ceiling, or scale effects? | |

Use the operational name in Results when construct validity is limited. Reserve broader labels for cases with an explicit validation argument.

## Evaluation labels are claims

Define the exact operation and axis before applying a broad evaluation label:

- **OOD** or **zero-shot:** identify what was held out, the reference
  distribution, and the selection boundary;
- **robust:** identify the perturbation set, endpoint, and stability criterion;
- **counterfactual** or **causal:** identify the intervention, comparison, and
  assumptions required for identification;
- **physical:** identify the measured quantity, governing constraint, or
  validation that earns the term;
- **real-time:** identify hardware, batch or query shape, measurement boundary,
  and latency criterion;
- **uncertainty:** identify what varies, how it is estimated, and what the
  reported interval or distribution represents.

If the study establishes only a narrower property, use the operational
description instead of the broader label.

## Independence and uncertainty checks

- Preserve pairing when observations share a source or condition.
- Resample clusters rather than rows when rows are dependent.
- Distinguish variation across observations from uncertainty in the estimator.
- Report distributional heterogeneity when a mean conceals important subgroups.
- Do not interpret overlap or non-overlap of error bars without knowing what they represent.
- Do not treat repeated optimization runs as independent evidence about population generality.
