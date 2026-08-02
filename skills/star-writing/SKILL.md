---
name: star-writing
description: Route and coordinate multi-stage research-paper work across initial paper orientation, project writing-ledger decisions, framing, literature, technical methods, evidence, drafting, polishing, review, and submission. Use for end-to-end journal, conference, or workshop workflows; paper-wide planning or revision; claim-evidence alignment; or associated artifacts spanning stages. Remain language-, field-, project-, and venue-neutral. Prefer focused star-writing-* skills for narrow tasks.
---

# STAR Writing

Build a research paper and its associated publication artifacts as a bounded,
auditable argument. Coordinate the focused skills without turning the workflow
into a fixed prose template.

## Start with the task contract

Before substantive analysis or any edit, establish through supplied context and
read-only inspection:

- the requested mode: explore, converge, audit, plan, preview, draft, revise,
  polish, or submit;
- the current manuscript or artifact snapshot;
- the paper or associated artifact type, audience, language, discipline, and venue
  constraints that materially affect form;
- the permitted scope and whether edits are authorized;
- locked content and concurrent writers;
- the research stage and whether evidence is provisional or final.

Treat “review,” “inspect,” and “discuss” as read-only unless the user also asks
for changes. Do not silently broaden a local edit into a scientific rewrite.

For paper-wide or high-stakes work, read
[constitution.md](references/constitution.md). Discover existing project state
and load only the task-relevant accepted projection. When no project ledger
exists, use [paper-contract.md](references/paper-contract.md) and
[terminology-and-symbols.md](references/terminology-and-symbols.md) as immutable
templates for a task-local record; do not create project state automatically.
Follow the
[Writing Ledger consumer contract](references/writing-ledger-contract.md) to
combine core propositions, concepts, terms, and symbols without creating a
competing aggregate file.
Use [decision-log.md](references/decision-log.md) only for an authorized record
of a material accepted supersession, not as the current state or evidence.
For full-artifact revision, exhaustive review, or finalization, read
[content-and-completion-gates.md](references/content-and-completion-gates.md).

Keep four layers separate:

- stable research-writing principles in the constitution;
- recurring author preferences in the polish skill's author style profile;
- current project facts and semantic decisions in the Project Writing Ledger;
- expiring venue rules in a live submission overlay.

Do not promote a personal style preference, project fact, or remembered venue
rule into a universal writing principle.

Skill evolution is a separate lifecycle. Feedback may adapt the current task or
create a task-local observation, but it does not authorize project evolution
state, persistent source changes, or canonical promotion-ledger writes. Keep
the paper controller responsible for the paper. After a material task, perform
a bounded learning check only when there was an explicit correction, accepted
nontrivial improvement, repeated friction, failure, or skill gap. A no-op is
valid; do not manufacture an update from a smooth session, silence, or generic
praise. When such a learning review is in scope, read the
[evidence-driven evolution policy](references/evolution-policy.md) and route to
`star-writing-evolve`. Do not interrupt a paper task for routine evolution
bookkeeping.

During paper tasks, bundled files under `references/` are immutable templates.
Do not write project facts or author preferences into the installed skill. With
explicit authorization, copy working state to paths relative to the resolved
project root:

- `.star-writing/paper-contract.md` for project facts and locks;
- `.star-writing/terminology-and-symbols.md` for canonical names, definitions,
  acronyms, and notation;
- `.star-writing/decision-log.md` for material accepted supersessions;
- `.star-writing/submission-overlays/<target>-<cycle>-<category>-<stage>.md` for
  expiring submission rules;
- `.star-writing/author-style-profile.md` for project-specific writing
  preferences.

Only `star-writing-evolve` may create authorized project-local learning state
under `.star-writing/evolution/`. Observations, candidates, evaluations,
decisions, and receipts there are inactive evidence. They do not constrain
paper writing, authorize canonical skill changes, or replace the Project
Writing Ledger.

Persistent state is optional. Read
[state-and-paths.md](references/state-and-paths.md) before discovering or
creating project state or a cross-project author profile. Do not use the
agent's launch directory as the project root merely because it is convenient.

Without authorization to create state files, maintain the same information in
the current task context.

For an authorized full-manuscript or multi-section task, route material semantic
decisions to `star-writing-ledger`. Use an existing ledger or keep proposed
entries task-local until the user accepts the relevant project-state write. A
named-file edit does not by itself authorize ledger creation or maintenance.

## Route to the focused skill

- Use `star-writing-start` to orient to a newly received or unfamiliar paper,
  identify its canonical snapshot and relevant sources, build a compact Paper
  Map, and recommend the next workflow without editing.
- Use `star-writing-ledger` to establish, reconcile, or persist core
  propositions, concept boundaries, canonical names, acronyms, labels, and
  symbols one decision at a time.
- Use `star-writing-frame` for the research problem, central insight, novelty,
  contribution, or story.
- Use `star-writing-literature` for field structure, closest-work comparison,
  citation verification, or positioning.
- Use `star-writing-method` for problem setup, information availability,
  notation, equations, algorithms, implementation alignment, or technical
  method exposition.
- Use `star-writing-evidence` for experiments, metrics, statistics, results,
  figures, tables, or primary/supporting evidence design.
- Use `star-writing-draft` to compose or restructure sections and complete
  manuscripts.
- Use `star-writing-polish` for precise, concise, natural wording or
  translation without scientific change.
- Use `star-writing-review` for skeptical pre-submission review, consistency
  audit, or rejection-risk analysis.
- Use `star-writing-submit` for current target rules, formatting, identity,
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

Read [interactive-revision.md](references/interactive-revision.md) when the
user wants a TUI-style change preview, approval before file edits, or legible
interactive presentation of technical formulas.

Read [principle-tags.md](references/principle-tags.md) whenever proposing or
reporting substantive target-artifact changes. Highlight the governing
principle in the author-facing rationale while keeping the tag outside the
target artifact and separate from the evidence for the change.

### Load the selected workflow

Routing is not complete until the selected skill body is read. Choose one
controller for the current stage, then load its sibling `SKILL.md` explicitly:

- [frame](../star-writing-frame/SKILL.md);
- [start](../star-writing-start/SKILL.md);
- [ledger](../star-writing-ledger/SKILL.md);
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
Treat Ground, Explore, and Converge as a loop rather than a waterfall. A new
hypothesis or rival explanation should name the uncertainty that matters, then
trigger only the literature, data, derivation, implementation, or experiment
check needed to resolve it.

1. **Orient.** Bind the task to the current files, evidence, mode, and edit
   boundary.
2. **Contract.** State the research object, available information, assumptions,
   output, scope, closest alternative, and current candidate claim or unresolved
   question. Reconcile any load-bearing conflict with accepted Writing Ledger
   entries before dependent writing.
3. **Ground.** Trace implementation facts, empirical results, mathematics,
   literature claims, and submission rules to the source responsible for each.
4. **Explore.** Use first-principles reasoning, grounded brainstorming, and
   thought experiments to generate alternatives without presenting them as
   established facts.
5. **Converge.** Compare candidate formulations, explanations, and contribution
   types against the closest work and available evidence. Record why rejected
   alternatives were rejected.
6. **Structure.** Build the claim–evidence map and reader-facing argument before
   optimizing sentences.
7. **Write.** Draft each unit for a defined inferential role; preserve
   uncertainty and boundaries.
8. **Audit.** Apply QA proportional to the edit: local, section, story,
   finalization, or submission. For a claimed full audit, traverse every
   applicable content unit in document order and record completion.
9. **Handoff.** Report what was confirmed, what changed, what remains
   unestablished, and what was verified. When a material learning signal was
   explicitly in scope, report its task-local or authorized project-local state;
   otherwise do not append a ritual evolution proposal.

## Enforce cross-stage constraints

- Do not write a stronger story than the evidence identifies.
- Apply the same evidential standard to supporting and adverse findings. Do not
  act as the paper's advocate or as a performatively hostile reviewer.
- Do not treat a metric name as proof of the construct it is meant to measure.
- Do not present novelty, validity, mechanism, and utility as interchangeable.
- Name every claimed axis of generality and every relevant boundary.
- Treat visuals derived from the same underlying results as complementary views,
  not independent confirmations.
- When the target defines primary and supporting artifacts, keep the primary
  artifact complete for its required central argument and use supporting
  artifacts only for permitted depth, reproduction, or secondary evidence.
- Make every retained content unit serve a necessary reader, evidence,
  technical, reproduction, or artifact role. Correctness alone does not earn
  inclusion.
- Verify, narrow, or omit uncertain detail. Do not elaborate low-confidence
  content into apparent authority.
- Keep internal audit caveats separate from reader-facing prose unless they
  prevent a material misinterpretation.
- Do not paste brainstorming, thought experiments, confidence labels, rejected
  alternatives, or reviewer dialogue into the target artifact. Promote only
  content that passes the evidence, necessity, and reader-role gates.
- Adapt organization and prose to the target language, discipline, audience,
  paper type, and venue. Do not impose English-language habits, one field's
  section sequence, or a main/supplement split when the target does not use them.
- Propagate changes to core definitions, terminology, numbers, and claims across
  all dependent sections and artifacts.
- Bind final readiness to the exact artifact hash. Regeneration invalidates
  binary-dependent checks.
- Explain substantive proposed or applied changes with the controlled,
  highlighted principle tags. Use one governing principle per item and at most
  one secondary governing principle or reasoning lens. Never let a tag replace
  source-grounded reasoning.

Stop prose work and investigate, narrow the claim, or request a decision when
the current snapshot is unknown, a headline result is untraceable, a citation
does not support its clause, a causal attribution lacks an isolating test, or a
concurrent edit makes safe modification impossible.

If the user explicitly requests exploratory drafting despite unresolved facts,
continue only with bounded claims and conspicuous placeholders. Do not present
that draft as verified or final.
