# Claim–evidence matrix

Use this matrix to determine the minimum evidence appropriate to a claim. Treat it as a starting point, then adapt it to the field and study design.

| Claim type | Minimum evidential requirement | Common invalid leap |
|---|---|---|
| Definition | Explicit object, scope, assumptions, and relation to existing terms | Treating a label as an operational definition |
| Mathematical property | Stated assumptions and a valid proof, derivation, or cited result | Extending a result beyond its assumptions |
| Implementation | Executed source, configuration, dependencies, and behavior check | Inferring implementation from the manuscript description |
| Feasibility or existence | A valid construction or demonstration under stated conditions | Generalizing one success to typical performance |
| Descriptive empirical | Appropriate sample, measurement procedure, and uncertainty or variability | Treating a selected case as population evidence |
| Comparative improvement | Comparable conditions, defined endpoint, effect size, uncertainty, and aggregation | Attributing a difference to the named method despite unequal information or budget |
| Mechanism or causality | Intervention, controlled contrast, identification argument, or theory that excludes relevant rivals | Explaining a system-level difference through an unisolated component |
| Robustness | Prespecified meaningful perturbations or replications across the claimed variation | Calling high average accuracy robust |
| Generality | Systematic variation along every claimed axis and explicit boundary conditions | Inferring domain, population, or task generality from one kind of diversity |
| Efficiency | End-to-end resource accounting under comparable hardware, software, workload, and quality | Reporting only one stage, theoretical complexity, or unmatched runtime |
| Practical utility | A relevant downstream decision, outcome, or validated workflow benefit | Recasting prospective usefulness as demonstrated impact |
| Reproducibility | Available data or generation route, code, environment, configuration, seeds or replication policy, evaluation, and provenance | Equating a repository skeleton or aggregate table with end-to-end reproduction |
| New metric | Formula, target construct, interpretation, invariances, sensitivity analysis, and failure modes | Assuming the metric measures the construct because of its name |

## Identification test

For each major claim, answer:

1. What observation would be expected if the claim were true?
2. What other explanation would produce the same observation?
3. Which design feature distinguishes those explanations?
4. At what unit does that distinction occur?
5. What residual uncertainty remains?

If question 3 has no answer, describe association or system-level difference rather than mechanism.

## Generality axes

Name the exact varied axes instead of using unqualified generality language. Possible axes include:

- population or sample source;
- task or endpoint;
- environment or domain;
- scale or resolution;
- time or operating regime;
- intervention or condition;
- method family;
- measurement instrument;
- resource budget.

Evidence along one axis does not establish another.
