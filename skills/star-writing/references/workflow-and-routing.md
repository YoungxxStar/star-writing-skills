# Workflow and Routing

Use this reference for requests that span multiple writing stages or involve
several collaborators.

## Contents

- [Select the work mode](#select-the-work-mode)
- [Choose the sequence](#choose-the-sequence)
- [State-machine gates](#state-machine-gates)
- [Transactional collaboration](#transactional-collaboration)
- [Stop conditions](#stop-conditions)

## Select the work mode

- **Explore:** use writing to clarify an idea; label it as provisional and do
  not let it enter the manuscript as established fact.
- **Converge:** challenge competing formulations, explanations, and
  contribution types against literature and evidence; record why one bounded
  account survives.
- **Audit:** inspect and report without editing.
- **Plan:** produce contracts, claim maps, outlines, or revision proposals.
- **Draft:** compose new authorized manuscript content from a stable research
  frame and evidence base.
- **Revise:** change authorized content while preserving the scientific
  boundary.
- **Polish:** improve language only; do not alter claims, evidence, numbers,
  notation, or citations.
- **Submit:** freeze content as appropriate, verify live rules, render, and
  inspect the package.

If the user asks to “look,” “review,” “compare,” or “discuss,” default to audit.
If a request mixes modes, state the boundary and order them deliberately.

## Choose the sequence

Use the minimum sequence that resolves the request:

- Unclear idea or novelty: frame, then literature.
- Several plausible stories or contribution types: frame and literature, then
  converge before drafting.
- Technical method, notation, or code–paper mismatch: method first, then
  evidence for claim impact and draft for authorized prose changes.
- Claim scope exceeds its proof or study design: evidence first, then frame or
  draft.
- Novelty depends on unidentified or abstract-only sources: literature before a
  definitive novelty statement.
- Existing section with structural problems: review, then draft, then polish.
- New section from an established contract and evidence map: draft, then
  polish.
- Existing section with sound logic but awkward language: polish only.
- Overall defensibility or paper-wide inconsistency: review controls the
  judgment, then route technical evidence issues to evidence and prose changes
  to draft or polish.
- Metrics, statistics, experiments, Results, or visuals without a whole-paper
  decision: evidence controls.
- Final package: review unresolved scientific risks before submit.

Do not polish unstable science. Do not redesign experiments merely because a
sentence is difficult to defend.

## State-machine gates

### 1. Orient

Identify the canonical files, current version, research stage, requested mode,
allowed scope, locked content, and concurrent edits.

Exit when the exact task snapshot and mutation boundary are known.

### 2. Contract

State the scientific, evidential, and reader contracts. Record canonical terms
and the closest alternative.

Exit when the core claim can be stated with its scope and qualifier.

### 3. Ground

Resolve each important statement against its responsible source. Mark claims as
established, supported but bounded, exploratory, provisional, or unsupported.

Exit when all headline claims, numbers, and citations are traceable.

### 4. Converge

Test candidate formulations, explanations, and contribution types against the
closest alternatives and the evidence. Update the decision log with the
previous understanding, new evidence, revised understanding, and affected
artifacts.

Exit when one bounded account survives and rejected alternatives are recorded.

### 5. Structure

Build the claim–evidence map and reader sequence. Assign each section,
paragraph, and visual an inferential role.

Exit when every major artifact advances a necessary claim and no major claim is
orphaned.

### 6. Write

Draft or revise according to section contracts. Preserve distinctions among
fact, measurement, inference, mechanism, and implication.

Exit when the requested scope is scientifically complete before surface polish.

### 7. Audit

Match QA to scope:

- local edit: facts, terminology, local logic, and scope;
- section rewrite: add reverse outline, claim–evidence alignment, and
  transitions;
- story revision: add cross-section propagation and abstract–conclusion
  consistency;
- finalization: add data, code, formula, citation, visual, and supplement
  consistency;
- submission: add current venue, rendering, anonymity, and package checks.

### 8. Handoff

Report:

- what was verified;
- what changed;
- what was intentionally preserved;
- what remains unsupported or provisional;
- what validation was run.

## Transactional collaboration

When multiple writers or agents share files:

1. Assign one writer per file or section; allow parallel read-only reviewers.
2. Record the starting file hash, scope, and lock.
3. Recheck the file immediately before writing.
4. If the hash changed, reread and rebase the proposed edit semantically.
5. Avoid unbounded global replacement on an active manuscript.
6. Inspect the semantic diff after merging, then compile or render.
7. Stage only the authorized scope; do not absorb another writer’s incomplete
   work.
8. Keep canonical terminology, frozen decisions, and removed content in a
   shared working contract.

Treat bundled references as immutable templates. Resolve optional project and
user state through the controller's state-and-path policy. Do not create or
modify persistent state when the user has requested read-only discussion.

## Stop conditions

Stop writing and investigate, narrow the claim, or ask for a material decision
when:

- the current artifact version cannot be established;
- the research object, information contract, or comparison is undefined;
- a headline number lacks provenance or a statistical contract;
- a citation does not support the clause;
- the design does not isolate the claimed mechanism;
- sources conflict on a material fact;
- a terminology change alters the scientific contract;
- a venue rule is recalled only from memory or an old cycle;
- a concurrent edit prevents safe modification.

An explicit request for an exploratory draft permits visible placeholders and
clearly bounded claims; it does not waive verification or authorize final
novelty, result, or priority language.

Resolve discoverable questions from the available sources before asking the
user. Ask only when the unresolved choice would materially change the work.
