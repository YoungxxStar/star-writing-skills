# Workflow and Routing

Use this reference for requests that span multiple writing stages or involve
several collaborators.

## Contents

- [Select the work mode](#select-the-work-mode)
- [Choose the sequence](#choose-the-sequence)
- [State-machine gates](#state-machine-gates)
- [Use the evolution side path](#use-the-evolution-side-path)
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
- **Preview:** present numbered proposed changes for approval without editing.
- **Draft:** compose new authorized manuscript content from a stable research
  frame and evidence base.
- **Revise:** change authorized content while preserving the scientific
  boundary.
- **Polish:** improve language only; do not alter claims, evidence, numbers,
  notation, or citations.
- **Submit:** freeze content as appropriate, verify live rules, render, and
  inspect the package.

If the user asks to “look,” “review,” “compare,” or “discuss,” default to audit.
If the user requests approval before editing, use preview before revise, polish,
or edit. If a request mixes modes, state the boundary and order them deliberately.

## Choose the sequence

Use the minimum sequence that resolves the request:

- Unclear idea or novelty: frame, then literature.
- Several plausible stories or contribution types: frame and literature, then
  converge before drafting.
- Technical method, notation, or code–paper mismatch: method first, then
  evidence for claim impact and draft for authorized prose changes.
- Conflicting core proposition, concept identity, canonical name, acronym, or
  symbol across locations: use ledger as the interaction controller, obtain the
  responsible frame, literature, method, or evidence judgment, then return to
  one-entry convergence before writing.
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
- Reusable workflow success, correction, failure, or better method: keep the
  active paper controller in place, then route the learning question to
  `star-writing-evolve`. Do not mix a paper edit and a skill-source mutation
  under one implicit authorization.

Do not polish unstable science. Do not redesign experiments merely because a
sentence is difficult to defend.

## State-machine gates

### 1. Orient

Identify the canonical files, current version, research stage, requested mode,
allowed scope, locked content, and concurrent edits.

Exit when the exact task snapshot and mutation boundary are known.

### 2. Contract

State the scientific, evidential, and reader contracts. Discover the Project
Writing Ledger and load its task-relevant accepted projection. Record unresolved
semantic choices rather than silently selecting a new term or symbol.

Exit when a provisional problem, scope, and candidate claim or unresolved
question are explicit enough to determine what should be grounded. Do not
freeze the paper's final thesis before exploration.

### 3. Ground

Resolve each important statement against its responsible source. Mark claims as
`established`, `bounded`, `exploratory`, `unsupported`, `contradicted`, or
`unresolved` using the constitution's claim-status vocabulary.

Exit when the current evidence base, responsible sources, and consequential
unknowns are explicit enough to guide exploration. Do not require an early idea
to have final headline claims.

### 4. Explore

Before convergence, use first-principles reasoning and grounded thought
experiments when the idea space is unsettled. Generate alternatives from the
current literature, data, and records; label speculation and investigate only
the uncertainties that affect selection.

Exit when the candidate accounts, assumptions, and discriminating questions
are explicit. Return to Ground for only the searches, analyses, derivations, or
implementation checks that could change their ranking.

### 5. Converge

Test candidate formulations, explanations, and contribution types against the
closest alternatives and the evidence. Record the previous understanding, new
evidence, revised understanding, and affected artifacts in the current task.
Update a persistent decision log only when the state policy and user
authorization permit it.

Exit when one bounded account survives and rejected alternatives are recorded.
If several accounts remain live, report the discriminator instead of forcing a
false resolution. Require every load-bearing claim selected for drafting to be
traceable or explicitly unresolved before Structure.

When convergence changes a core proposition, concept, name, or symbol, route
the single accepted entry to `star-writing-ledger` before dependent writing.
The project-state update and manuscript propagation remain separate actions.

### 6. Structure

Build the claim–evidence map and reader sequence. Assign each section,
paragraph, and visual an inferential role.

Exit when every major artifact advances a necessary claim and no major claim is
orphaned.

### 7. Write

Draft or revise according to section contracts. Preserve distinctions among
fact, measurement, inference, mechanism, and implication.

Exit when the requested scope is scientifically complete before surface polish.

### 8. Audit

Match QA to scope:

- local edit: facts, terminology, local logic, and scope;
- section rewrite: add reverse outline, claim–evidence alignment, and
  transitions;
- story revision: add cross-section propagation and abstract–conclusion
  consistency;
- finalization: add data, code, formula, citation, visual, and permitted
  supporting-artifact consistency;
- submission: add current target rules and only the applicable rendering,
  identity, form, and package checks.

### 9. Handoff

Report:

- what was verified;
- what changed;
- what was intentionally preserved;
- what remains exploratory, unsupported, contradicted, or unresolved;
- what validation was run.

## Use the evolution side path

Evolution is not a paper-writing mode or gate. It runs beside the active task
and must not silently change its controller or artifact scope. Use
`star-writing-evolve` to reconstruct feedback, test whether it exposes an
execution lapse or reusable rule gap, and implement persistent skill-source
changes only with explicit authorization.

1. Adapt the current task to explicit feedback when safe.
2. Record a reusable lesson as a task-local candidate rather than a rule.
3. Route an explicit learning request to `star-writing-evolve` for audit or
   planning.
4. Persist an identified candidate only after the user separately authorizes
   that ledger write; persistence does not activate it.
5. Enter evolve mode for an active-rule change only after the user authorizes
   the identified development source and change scope.
6. Include local read-only structural checks in the authorized write, while
   treating stateful or external validation, versioning, commit, installation,
   push, and release as distinct states and permissions.

Read the
[evolution policy](evolution-policy.md) for signal interpretation, scope
placement, authorization, conflict resolution, regression testing, and
concurrent evolution.

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
9. Let `star-writing-ledger` own entry-level reconciliation. Other skills may
   propose a task-local candidate but must not silently rewrite project state.

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
- a submission rule is recalled only from memory or an old cycle;
- a concurrent edit prevents safe modification.

An explicit request for an exploratory draft permits visible placeholders and
clearly bounded claims; it does not waive verification or authorize final
novelty, result, or priority language.

Resolve discoverable questions from the available sources before asking the
user. Ask only when the unresolved choice would materially change the work.
