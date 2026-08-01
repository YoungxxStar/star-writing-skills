# Method and Notation Audit

Use this worksheet when method correctness depends on several representations,
stages, equations, algorithms, or implementation paths.

## Contents

- [Method snapshot](#method-snapshot)
- [Information availability matrix](#information-availability-matrix)
- [Object and notation ledger](#object-and-notation-ledger)
- [Equation audit](#equation-audit)
- [Procedure-to-implementation map](#procedure-to-implementation-map)
- [Capability status](#capability-status)
- [Mechanism status](#mechanism-status)
- [Main-to-supplement allocation](#main-to-supplement-allocation)
- [Repair order](#repair-order)

## Method Snapshot

```text
Manuscript and revision:
Implementation or protocol and revision:
Configuration:
Data interface:
Evaluation interface:
Requested audit scope:
Locked content:
Unavailable sources:
```

## Information Availability Matrix

| Quantity | Meaning | Preparation | Development or training | Selection | Use or inference | Evaluation only | Provenance |
|---|---|---|---|---|---|---|---|

Assign one or more roles:

- observed;
- prescribed or controlled;
- derived from available information;
- estimated or learned;
- latent;
- target or supervised;
- evaluation-only;
- oracle or privileged.

For every derived quantity, state its dependencies. A quantity is not available
merely because its name sounds like metadata or context.

## Object and Notation Ledger

| Symbol | Object | Type and shape | Domain or index set | Unit | Availability | First definition | Used in |
|---|---|---|---|---|---|---|---|

Check:

- one symbol has one meaning;
- vectors, fields, sets, distributions, parameters, and indices are distinct;
- normalized and physical quantities are distinguishable;
- time, stage, participant, specimen, site, component, and sample indices cannot
  be confused;
- every acronym and operator is defined;
- dimensions and domains remain consistent across equations.

## Equation Audit

For each equation, record:

| Equation | Role | Inputs | Output | Assumptions | Shape or unit check | Implementation or proof source | Status |
|---|---|---|---|---|---|---|---|

Classify the role as:

- definition;
- problem objective;
- formal or computational operation;
- loss or estimator;
- approximation;
- theorem or property;
- metric;
- explanatory schematic.

Flag equations that:

- introduce an undefined object;
- omit a consequential operation;
- imply a stronger mathematical property than the implementation provides;
- use an equality where an approximation or definition is intended;
- use notation only once without improving understanding;
- conflict with the algorithm, diagram, caption, or code.

## Procedure-to-Implementation Map

| Scientific step | Procedure or algorithm step | Implementation or protocol source | Configuration | Edge cases | Verified |
|---|---|---|---|---|---|

Check:

- true loops and stopping conditions;
- initialization and identity behavior;
- ordering of transformations;
- masking, padding, interpolation, and normalization;
- development-only and use-only branches, including training or inference;
- stochasticity, randomization, and replication handling;
- selection, caching, and preprocessing;
- output reconstruction or readout.

Do not convert implementation chronology directly into the paper's explanation.
Group operations by scientific role after verifying their executed order.

## Capability Status

| Claimed capability | Design permits | Current configuration enables | Executed path uses | Evaluation tests | Result establishes | Allowed wording |
|---|---|---|---|---|---|---|

Require evidence at each transition. Do not describe a possible interface,
disabled option, unused code path, or unevaluated objective as a demonstrated
capability.

## Mechanism Status

| Proposed mechanism | Implemented operation | Direct identifying evidence | Status | Allowed wording |
|---|---|---|---|---|

Use statuses:

- implemented;
- directly isolated;
- supported but bounded;
- inferred;
- intended;
- unresolved.

## Main-to-Supplement Allocation

Keep a technical item in the main paper when removing it would prevent a reader
from understanding the information contract, mechanism, assumption, or central
claim. Move detail when it extends reproduction or implementation-specific
depth without carrying the main inference.

## Repair Order

1. Resolve unavailable or leaked information.
2. Resolve contradictions among problem, equation, algorithm, diagram, and code.
3. Resolve undefined objects, shapes, units, and assumptions.
4. Calibrate mechanism and generality claims.
5. Simplify notation and prose.
6. Move secondary detail to supplementary material.
