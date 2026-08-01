---
name: star-writing
description: Route and coordinate multi-stage research-writing work across framing, literature, technical methods, evidence, drafting, polishing, review, and submission. Use for end-to-end paper workflows, paper-wide planning or revision, claim-evidence alignment across sections, or ambiguous manuscript requests that span more than one writing stage. Prefer the focused star-writing-* skills for narrow single-stage tasks.
---

# STAR Writing

Build a research paper as a bounded, auditable argument. Coordinate the focused
skills without turning the workflow into a fixed prose template.

## Start with the task contract

Before reading or editing, establish:

- the requested mode: explore, converge, audit, plan, draft, revise, polish, or
  submit;
- the current manuscript or artifact snapshot;
- the permitted scope and whether edits are authorized;
- locked content and concurrent writers;
- the research stage and whether evidence is provisional or final.

Treat “review,” “inspect,” and “discuss” as read-only unless the user also asks
for changes. Do not silently broaden a local edit into a scientific rewrite.

For paper-wide or high-stakes work, read
[constitution.md](references/constitution.md). Create or refresh the working
record from [paper-contract.md](references/paper-contract.md) when facts,
terminology, evidence, or multiple collaborators can drift.
Use [decision-log.md](references/decision-log.md) when new evidence changes a
material interpretation, term, claim, comparison, or artifact.
For full-artifact revision, exhaustive review, or finalization, read
[content-and-completion-gates.md](references/content-and-completion-gates.md).

Keep four layers separate:

- stable research-writing principles in the constitution;
- recurring author preferences in the polish skill's author style profile;
- current project facts and decisions in the paper contract;
- expiring venue rules in a live submission overlay.

Do not promote a personal style preference, project fact, or remembered venue
rule into a universal writing principle.

Bundled files under `references/` are immutable templates. Do not write
project facts or author preferences into the installed skill. With explicit
authorization, copy working state to paths relative to the resolved project
root:

- `.star-writing/paper-contract.md` for project facts and locks;
- `.star-writing/decision-log.md` for changed interpretations;
- `.star-writing/venue-overlays/<venue>-<year>-<track>.md` for expiring rules;
- `.star-writing/author-style-profile.md` for project-specific writing
  preferences.

Persistent state is optional. Read
[state-and-paths.md](references/state-and-paths.md) before discovering or
creating project state or a cross-project author profile. Do not use the
agent's launch directory as the project root merely because it is convenient.

Without authorization to create state files, maintain the same information in
the current task context.

## Route to the focused skill

- Use `star-writing-frame` for the research problem, central insight, novelty,
  contribution, or story.
- Use `star-writing-literature` for field structure, closest-work comparison,
  citation verification, or positioning.
- Use `star-writing-method` for problem setup, information availability,
  notation, equations, algorithms, implementation alignment, or technical
  method exposition.
- Use `star-writing-evidence` for experiments, metrics, statistics, results,
  figures, tables, or main–supplement evidence design.
- Use `star-writing-draft` to compose or restructure sections and complete
  manuscripts.
- Use `star-writing-polish` for precise, concise, natural wording or
  translation without scientific change.
- Use `star-writing-review` for skeptical pre-submission review, consistency
  audit, or rejection-risk analysis.
- Use `star-writing-submit` for current venue rules, formatting, anonymization,
  artifacts, reproducibility, or package checks.

When a request asks whether a section or paper is defensible overall, let
`star-writing-review` control the judgment and use `star-writing-evidence` for
the technical evidence audit. When the request is specifically about study
design, metrics, statistics, results, or visuals, let `star-writing-evidence`
control. Bound theorem or empirical scope before using `star-writing-frame` to
strengthen the story.

Read [workflow-and-routing.md](references/workflow-and-routing.md) when the
request spans skills, the proper order is unclear, or collaborators are editing
in parallel.

### Load the selected workflow

Routing is not complete until the selected skill body is read. Choose one
controller for the current stage, then load its sibling `SKILL.md` explicitly:

- [frame](../star-writing-frame/SKILL.md);
- [literature](../star-writing-literature/SKILL.md);
- [method](../star-writing-method/SKILL.md);
- [evidence](../star-writing-evidence/SKILL.md);
- [draft](../star-writing-draft/SKILL.md);
- [polish](../star-writing-polish/SKILL.md);
- [review](../star-writing-review/SKILL.md);
- [submit](../star-writing-submit/SKILL.md).

Load only references required by the active task. When several stages are
needed, complete them in dependency order rather than merging incompatible
output contracts. A validator may inspect another dimension, but the controller
owns the current judgment and deliverable.

## Run the research-to-paper gates

Skip gates already satisfied and revisit any gate invalidated by new evidence.

1. **Orient.** Bind the task to the current files, evidence, mode, and edit
   boundary.
2. **Contract.** State the research object, available information, assumptions,
   output, scope, closest alternative, and central claim.
3. **Ground.** Trace implementation facts, empirical results, mathematics,
   literature claims, and submission rules to the source responsible for each.
4. **Converge.** Compare candidate formulations, explanations, and contribution
   types against the closest work and available evidence. Record why rejected
   alternatives were rejected.
5. **Structure.** Build the claim–evidence map and reader-facing argument before
   optimizing sentences.
6. **Write.** Draft each unit for a defined inferential role; preserve
   uncertainty and boundaries.
7. **Audit.** Apply QA proportional to the edit: local, section, story,
   finalization, or submission. For a claimed full audit, traverse every
   applicable content unit in document order and record completion.
8. **Handoff.** Report what was confirmed, what changed, what remains
   unestablished, and what was verified.

## Enforce cross-stage constraints

- Do not write a stronger story than the evidence identifies.
- Do not treat a metric name as proof of the construct it is meant to measure.
- Do not present novelty, validity, mechanism, and utility as interchangeable.
- Name every claimed axis of generality and every relevant boundary.
- Treat visuals derived from the same underlying results as complementary views,
  not independent confirmations.
- Keep the main paper scientifically complete; use supplementary material for
  depth, reproducibility, and secondary evidence.
- Make every retained content unit serve a necessary reader, evidence,
  technical, reproduction, or artifact role. Correctness alone does not earn
  inclusion.
- Verify, narrow, or omit uncertain detail. Do not elaborate low-confidence
  content into apparent authority.
- Keep internal audit caveats separate from reader-facing prose unless they
  prevent a material misinterpretation.
- Propagate changes to core definitions, terminology, numbers, and claims across
  all dependent sections and artifacts.
- Bind final readiness to the exact artifact hash. Regeneration invalidates
  binary-dependent checks.

Stop prose work and investigate, narrow the claim, or request a decision when
the current snapshot is unknown, a headline result is untraceable, a citation
does not support its clause, a causal attribution lacks an isolating test, or a
concurrent edit makes safe modification impossible.

If the user explicitly requests exploratory drafting despite unresolved facts,
continue only with bounded claims and conspicuous placeholders. Do not present
that draft as verified or final.
