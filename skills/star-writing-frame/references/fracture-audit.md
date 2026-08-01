# Fracture Audit

Use this reference to diagnose a paper-level frame or a research idea whose story repeatedly changes. Select only the checks relevant to the claim under review.

## Contract Map

| Stage | Required content | Diagnostic questions |
| --- | --- | --- |
| Objective | Scenario, stakeholder or scientific audience, decision or inquiry, and scientific, theoretical, practical, or decision value | What changes if the problem is solved? Who or what benefits or learns? |
| Formulation | Object, known quantities, unknown quantities, and required outcome | Is the task defined without the proposed method? Is success measurable? |
| Information | Availability, timing, provenance, and exclusions | Is every input available at use time? Is privileged information disclosed? |
| Design | Principle, mechanism, interfaces, and assumptions | Does each major choice answer a stated requirement? |
| Inference | Actual operating conditions and outputs | Does use time match the formulation and training assumptions? |
| Evaluation | Estimand, comparison, independent unit, metric, and scope | Does the protocol test the stated claim under a fair contrast? |
| Use | Established implication and downstream boundary | Is utility measured directly or only proposed? |

When the frame includes a “why now” claim, verify the enabling change and its
timing. New data, measurement, theory, computation, evaluation capability, or
operating conditions can create an opportunity. A generic claim that the topic
is increasingly important does not.

## Common Handoff Fractures

### Objective to Formulation

- The motivation concerns one outcome, but the formal task optimizes a proxy with no stated link.
- The testbed is presented as the general problem.
- The problem exists only after assuming the proposed solution.

### Formulation to Information

- The formulation omits when inputs become available.
- Training or evaluation uses information unavailable in deployment.
- The proposed method and alternatives receive different information.

### Information to Design

- A component is introduced without an information or representation requirement.
- The method name implies a capability not present in the operation.
- Extra information, capacity, or computation is mistaken for a mechanism.

### Design to Inference

- Training depends on annotations, interventions, or future quantities absent at use time.
- The method is described as portable, but hidden adapter assumptions change across systems.
- The inference output differs from the formal target.

### Inference to Evaluation

- Evaluation provides easier inputs, oracle selection, or leaked statistics.
- The metric measures a proxy rather than the claimed construct.
- The reported sample count hides correlated or nested observations.

### Evaluation to Use

- Benchmark accuracy is promoted to downstream utility without a downstream test.
- Sensitivity is promoted to correctness, or correlation to mechanism.
- Breadth across one variation axis is promoted to unrestricted generalization.
- Component-level interpretation is drawn from a multi-component treatment.

## Contribution Chain Audit

For each link, record `verified`, `observed`, `inferred`, `intended`, or `unresolved`.

| Link | Audit question | Frequent overreach |
| --- | --- | --- |
| Assumption -> Violation | Is the assumption documented, and does the target setting violate it? | Criticizing a strawman |
| Violation -> Failure | Is the failure measured, or merely plausible? | Writing a hypothesis as an observation |
| Failure -> Missing capability | Have rival explanations been tested? | Naming the proposed feature as the only remedy |
| Missing capability -> Design principle | Does the principle follow, or is it one optional choice? | Calling a design necessary |
| Design principle -> Mechanism | Does the implemented operation realize the principle? | Inferring behavior from a label |
| Mechanism -> Direct evidence | Does the comparison isolate the mechanism? | Attributing a complete-treatment gain to one part |

## Rival-Explanation Check

Before assigning causality, test whether the outcome could follow from:

- additional or earlier information;
- greater capacity or computation;
- different training exposure or supervision;
- unequal tuning or selection;
- a changed metric, subset, or aggregation;
- leakage or privileged evaluation inputs;
- a simpler mechanism.

If these remain viable, report the observed system-level effect and mark the mechanism as an interpretation.

## Fracture Report

Use a compact table:

| Handoff or link | Status | Evidence | Consequence | Required repair |
| --- | --- | --- | --- | --- |

Prioritize the earliest fracture. Downstream prose usually stabilizes after the upstream contract is corrected.

Do not force the final paper to display every stage or link explicitly. Use the audit to protect meaning while allowing the author to choose emphasis, order, and voice.
