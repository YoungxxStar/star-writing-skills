---
name: star-writing-start
description: Orient to a newly received or unfamiliar research paper, manuscript, or publication project before deeper writing work. Use when the user asks to start with, understand, learn, inspect, or onboard an agent to a paper; identify the canonical manuscript and relevant materials; or establish a compact Paper Map and next workflow. This controller is always read-only. Do not use for an already scoped review, method, evidence, drafting, polishing, or submission task; route any authorized downstream action to its responsible skill.
---

# STAR Writing: Start

Enter an unfamiliar paper once, with enough structure that later work does not
require the author to repeat a long briefing. Establish the current artifact,
its argument, its evidence boundary, and the next responsible skill. Do not
turn onboarding into a premature review or rewrite.

## Accept a minimal handoff

Treat a paper path, attached artifact, repository path, or clearly identified
current manuscript plus a short goal as sufficient to begin. Do not demand a
questionnaire or ask the user to restate facts that can be discovered safely.

Operate only in `audit` mode. Interpret `start`, `read`, `understand`, `get
familiar with`, and `look through` as read-only. Even when the user also
authorizes a later mutation, keep this controller read-only and hand the
authorized scope to the responsible downstream skill after orientation. A
request to start work on a paper does not by itself authorize manuscript edits,
project-state creation, external publication, or Git actions.

When no artifact is named, inspect the available task context for a unique
candidate. Do not equate the launch directory with the paper root merely
because it is convenient. If several current manuscripts or project roots
remain plausible, report the candidates and ask one decision-changing
question rather than selecting silently.

## Bind the paper snapshot

Before interpreting content, resolve as far as the available sources allow:

- the project root or standalone artifact;
- the canonical manuscript entry point and current source or rendered snapshot;
- the paper type, language, audience, research stage, and target when stated;
- the user's immediate purpose and requested depth;
- locked artifacts, provisional evidence, and concurrent writers;
- the source types available for implementation, empirical results,
  mathematics, literature, reproducibility, and submission requirements.

Record a hash, revision, or other stable identity when consequential and
available. If source and rendered artifacts disagree, identify both and do not
guess which one is current.

For paper-wide orientation, read the shared
[constitution](../star-writing/references/constitution.md). Follow the
[Writing Ledger consumer contract](../star-writing/references/writing-ledger-contract.md):
discover the exact project paths, load only task-relevant accepted entries, and
do not create a ledger or launch a ledger interview automatically. An absent
ledger does not block orientation.

## Read in evidence order

Read the canonical manuscript in document order. Include every section and the
reader-visible roles of equations, tables, figures, captions, and references
when the requested object is a complete paper. For a rendered-only artifact,
traverse every page. For a named section or partial artifact, keep the map
explicitly local.

Inspect associated material only when it can change understanding of a
load-bearing claim:

1. current manuscript source and rendered artifact;
2. present supporting, rebuttal, or appendix material;
3. figure, table, bibliography, and result sources;
4. implementation, configuration, data, analysis, and experiment records;
5. existing research or literature notes.

Do not recursively absorb an entire repository merely because it exists.
Search for responsible sources, then read the relevant files sufficiently to
support the map. Distinguish manuscript claims from facts independently
verified in code, data, mathematics, or literature. Do not browse for or
download literature by default; route a consequential citation or novelty
question to `star-writing-literature`.

## Build the Paper Map

Return a compact map at the depth supported by the available artifacts:

1. **Snapshot and scope** — canonical artifact, identity, stage, target if
   known, requested purpose, and material actually inspected.
2. **Research contract** — research object, problem or inquiry, available
   information, intervention or method, output or estimand, assumptions, and
   scope.
3. **Motivation chain** — why the problem matters, the unresolved obstacle,
   the central intellectual move, and why that move addresses the obstacle.
4. **Argument spine** — the sequence by which the paper asks the reader to
   accept its central conclusion.
5. **Claims and evidence** — each load-bearing proposition, its claimed
   contribution type, responsible evidence, and current status. Use
   `established`, `bounded`, `exploratory`, `unsupported`, `contradicted`, or
   `unresolved` only as warranted.
6. **Concept and notation candidates** — recurring core concepts, terms,
   acronyms, labels, and symbols, including material conflicts. Keep these
   task-local unless the user later authorizes `star-writing-ledger`.
7. **Initial leverage and risk** — the strongest supported feature, the most
   consequential unresolved weakness, and uncertainties that could change the
   next task. Do not substitute a full reviewer report.
8. **Next route** — recommend the smallest responsible STAR Writing skill and
   one short invocation.

Scale the map to the artifact. Do not fill headings with generic prose, repeat
the abstract, dump a directory inventory, or claim complete understanding of
sources that were not inspected. State unavailable and unverified boundaries
plainly.

## Route the next task

Recommend and hand off the next stage; do not execute it from this controller.
If the original request already authorizes downstream work, record its exact
scope in the handoff and route it to the responsible skill:

- `star-writing-ledger` for accepted propositions, concepts, terms, and symbols;
- `star-writing-frame` for motivation, problem formulation, or contribution logic;
- `star-writing-literature` for closest work, citations, or novelty;
- `star-writing-method` for information availability, equations, procedures,
  or implementation alignment;
- `star-writing-evidence` for study design, metrics, results, figures, or tables;
- `star-writing-draft` for authorized composition or restructuring;
- `star-writing-polish` for meaning-preserving language work;
- `star-writing-review` for a purpose-specific skeptical or consistency review;
- `star-writing-submit` for live target rules and package readiness.

Do not load the shared
[evolution policy](../star-writing/references/evolution-policy.md) during
ordinary orientation. If the user explicitly asks the plugin to learn from the
episode, retain only a task-local observation and route that separate question
to `star-writing-evolve`.

Use the shared
[principle registry](../star-writing/references/principle-tags.md) only when the
handoff recommends a substantive corrective action. Keep the highlighted tag
separate from the source-grounded reason; do not tag descriptive Paper Map
entries or use a tag as evidence.

## Return a bounded handoff

Lead with the paper's central contract, not the reading process. End with:

- files or pages inspected;
- claims or sources not verified;
- ambiguities that require an author decision;
- one recommended next skill and a short ready-to-use prompt.

Do not modify files, create `.star-writing` state, initialize an evolution
workspace, or continue into rewriting merely to make the onboarding feel
complete. If the artifact changes during orientation, rebind the map to the
latest snapshot before reporting.
