---
name: star-writing-method
description: Audit or revise technical or methodological exposition in research papers by aligning problem setup, information availability, notation, equations, procedures, diagrams, and executed or documented practice. Use to verify symbols and operations, distinguish information by stage, map formal descriptions to implementation, diagnose unavailable information, simplify without changing the method, or allocate detail across main and permitted supporting artifacts. Default to read-only audit unless edits are requested.
---

# STAR Writing: Technical Method

Treat the Method section as a reconstructable technical contract. A polished
formula does not validate an implementation, and implementation behavior does
not by itself justify the paper's abstraction or claim.

Do not load the
[shared evolution policy](../star-writing/references/evolution-policy.md) for
ordinary paper work. If the user explicitly asks the plugin to learn, or this
task exposes a material, plausibly reusable success, correction, or gap, keep
this skill responsible for the paper, retain only a task-local candidate, and route plugin
maintenance to `star-writing-evolve`. Feedback alone cannot authorize a source
change.

## Set the mode and source boundary

- Use **audit** by default. Inspect and report without modifying manuscript,
  code, configuration, diagrams, or supplementary material.
- Use **revise** only when the user explicitly requests technical or manuscript
  changes.
- Identify the exact manuscript, implementation or protocol, configuration,
  data interface, and study snapshot.
- Preserve author locks and concurrent edits.
- Mark unavailable sources rather than inferring method details from prose.

Read
[references/method-and-notation-audit.md](references/method-and-notation-audit.md)
for a full technical audit or when several representations, stages, or
interfaces interact.

## Reconstruct the method contract

Recover the method independently of its name:

1. objective or estimand;
2. mathematical or scientific objects;
3. available and unavailable information at each stage;
4. input, output, assumptions, and operating conditions;
5. sequence of transformations;
6. estimated or learned, fixed, derived, and evaluation-only quantities;
7. interfaces between components;
8. estimation, transformation, optimization, decision, and readout procedures;
9. claimed mechanism and tested effect.

Write a compact end-to-end map:

`available information -> representation -> operation -> intermediate state -> output -> evaluation`

Locate the first point at which the manuscript, equations, diagram, algorithm,
or implementation disagrees.

## Audit information availability

For every quantity, record whether it is available during:

- data construction or study preparation;
- development or training;
- selection or validation;
- use or inference;
- evaluation only.

Record its provenance and whether it is observed, prescribed, derived,
estimated or learned, latent, supervised, or privileged. Flag:

- target-derived inputs at use time;
- statistics computed from held-out outcomes;
- evaluation-only quantities entering prediction;
- alternatives receiving different information;
- temporal or causal ordering inconsistent with the stated task.

Do not hide an availability mismatch through a broader term such as context,
condition, descriptor, or prior.

## Audit notation and equations

Before substantive work, follow
[the Writing Ledger contract](../star-writing/references/writing-ledger-contract.md).
Load only the relevant accepted concepts, terms, and symbols, including type,
shape, domain, unit, availability, responsible source, and first definition.
Build a task-local projection when no ledger exists. Method work verifies or
proposes concept, term, or symbol candidates with temporary referent keys;
`star-writing-ledger` owns persistent project decisions and stable-ID
assignment.

Apply a value gate before a definition gate. First ask whether the equation,
operator, auxiliary quantity, or symbol is needed to understand, evaluate, or
reproduce a material part of the method. Remove dispensable formalism; explain
a necessary operation in prose when notation adds more cognitive load than
precision. Require complete definitions only for objects that survive this
gate.

For every equation:

- define all symbols and operators;
- state dimensions, domains, indices, and quantifiers needed for interpretation;
- verify type and dimensional compatibility;
- distinguish definitions, assumptions, objectives, approximations, and derived
  results;
- identify omitted normalization, masking, boundary, padding, or selection
  operations that change behavior;
- map the equation to the implementation or proof source;
- remove notation that does not support later reasoning.

Treat unexplained exact counts and constants as notation defects. Decompose a
number into meaningful factors, identify its source or role, replace it with a
justified scale or range, or remove it. Do not leave a reader to infer why a
precise value appears.

Use the simplest formalism that preserves the mechanism. Do not simplify away
an input, constraint, qualifier, or operation required to reproduce the method.

When discussing formulas interactively, follow
[the TUI output rules](../star-writing/references/interactive-revision.md): keep
important equations on separate lines, wrap them at logical operators, and
define symbols close to their first displayed use.

## Audit procedures, algorithms, and implementation

For each algorithmic step, identify:

- input and output;
- loop, recursion, optimization, or stopping condition;
- deterministic versus learned behavior;
- design parameters or hyperparameters and whether they are principled, tuned,
  or conventional;
- treatment of invalid, empty, padded, missing, or boundary cases;
- corresponding protocol, instrument, analysis, or code path and configuration;
- computational or memory implication when claimed.

Replace internal run names, flags, version labels, and debugging language with
reader-facing operations. Do not replace a scientifically meaningful
implementation detail with a vague conceptual label.

## Calibrate mechanism claims

Separate:

- capability permitted by the general design;
- capability enabled by the current configuration;
- operation executed by the actual procedure or code path;
- capability evaluated by the reported study;
- effect established by the resulting evidence;
- mechanism implemented;
- design purpose;
- effect isolated by an ablation or intervention;
- system-level effect when several components change jointly;
- plausible but untested explanation.

Do not propagate certainty down this chain. A general equation or optional
interface does not show that a configuration activates it. An implemented
operation does not show that the evaluation tests it, and an evaluation target
does not show that the result establishes the capability.

Name a method from its actual operation. Terms implying physics, causality,
adaptivity, robustness, interpretation, or universality require matching
definitions and evidence.

Route result attribution, statistical identification, or metric validity to
`star-writing-evidence`. Route novelty relative to prior methods to
`star-writing-literature`. Route authorized manuscript revision to
`star-writing-draft` after the technical contract is stable.

## Allocate technical detail across permitted artifacts

Keep in the paper:

- problem and information contract;
- core objects and notation;
- decisive operations and interfaces;
- assumptions needed to interpret claims;
- enough mechanism to understand the contribution.

When the target permits supporting material, use it for:

- exhaustive hyperparameters;
- routine derivations;
- implementation-, instrument-, or apparatus-specific details;
- full pseudocode and implementation tables;
- secondary diagnostics and edge-case handling.

Do not invent supporting material or move a definition,
unavailable-information disclosure, or operation needed to trust the central
method out of the paper.

## Deliver the result

For an **audit**, return:

1. the reconstructed method contract;
2. an information-availability matrix;
3. a notation and equation defect list;
4. a manuscript-to-procedure or implementation map;
5. mechanism claims with epistemic status;
6. prioritized repairs, distinguishing prose, technical, and evidence changes.

For a **revision**, perform the compact audit first, then provide:

1. the revised technical passage, equation, algorithm, or structure;
2. one
   [highlighted governing principle](../star-writing/references/principle-tags.md)
   for each substantive change or coherent group, followed by its concrete
   implementation, proof, data, or reader-facing reason;
3. the scientific meaning and interfaces preserved;
4. definitions or inconsistencies corrected;
5. unresolved code, proof, data, or evidence dependencies.

Do not claim that a method is understood merely because its prose compiles, its
protocol is documented, or its implementation executes.
