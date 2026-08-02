# STAR Writing Skills

STAR Writing Skills is a cross-disciplinary, cross-language Codex plugin for
building defensible research papers and their associated supplements,
rebuttals, and release artifacts. It coordinates framing, literature, methods,
evidence, drafting, polishing, review, and live submission checks without
binding the workflow to a research field, project, language, venue, or fixed
paper template.

## Architecture

The plugin contains one router and eight focused skills.

| Skill | Owner of |
|---|---|
| `star-writing` | Multi-stage coordination and paper-wide or cross-artifact requests |
| `star-writing-frame` | First-principles motivation, problem formulation, novelty, and argument spine |
| `star-writing-literature` | Closest work, citation support, and positioning |
| `star-writing-method` | Information availability, notation, equations, procedures, and implementation alignment |
| `star-writing-evidence` | Study design, metrics, statistics, results, figures, tables, and claim-evidence alignment |
| `star-writing-draft` | Drafting, restructuring, and paper-type-appropriate evidence allocation |
| `star-writing-polish` | Meaning-preserving language improvement and translation |
| `star-writing-review` | Purpose-specific, adversarial, and consistency review |
| `star-writing-submit` | Live requirements, rendering or forms, identity, and packaging |

Use the router for work spanning several stages. Use a focused skill when one
owner clearly controls the requested deliverable.

## Working model

Use only the stages the task needs:

`Orient -> Contract -> [Ground <-> Explore] -> Converge -> Structure -> Write -> Audit -> Handoff`

Exploration uses current research, data, and records to generate alternatives;
each consequential uncertainty returns to targeted grounding. Convergence tests
the surviving accounts against the closest work and available evidence before
drafting. Submission is a live, target-specific audit layered onto a stable
paper and its associated artifacts.

Brainstorms, thought experiments, confidence labels, and rejected alternatives
remain in the working record. Only necessary, adequately supported content is
promoted into manuscript prose.

Substantive revision proposals and applied-change summaries expose their
governing rule through a bold, controlled tag such as **[SUPPORT-GATE]** or
**[CONTRACT-ALIGNMENT]**. When useful, a separate reasoning lens such as
**[CONFIDENCE-GATE]** or **[MOTIVATION-AS-STORY]** explains how the issue was
found. Canonical ASCII tags remain stable across languages, disciplines,
projects, venues, paper types, and associated artifact types; their source-grounded explanations
follow the interaction language. Tags are interaction metadata, never paper or
submission content and never scientific evidence.

For high-stakes work, every retained content unit must serve a necessary
reader, evidence, technical, reproduction, or artifact role. Full audits
traverse the artifact in document order rather than relying on searches alone.
Final readiness is bound to the exact rendered or packaged hash; regeneration
invalidates binary-dependent checks.

Mode words matter:

- review, inspect, audit, and discuss are read-only by default;
- preview shows numbered proposed changes but does not modify source files;
- rewrite returns revised text but does not modify a file;
- edit or revise a named file authorizes changes only within the stated scope;
- polish preserves claims, evidence, numbers, citations, notation, and
  scientific terminology.

## Install

Install the plugin as one bundle. Do not copy the nine skills separately or
hand-edit marketplace JSON.

Clone or download this repository first. For a private GitHub checkout over
SSH, for example:

```bash
git clone git@github.com:<owner>/star-writing-skills.git
```

For a first personal installation, run these commands from Codex's bundled
`plugin-creator` skill root:

```bash
python3 scripts/create_basic_plugin.py star-writing-skills --with-marketplace
cp -a /absolute/path/to/star-writing-skills/. ~/plugins/star-writing-skills/
python3 scripts/validate_plugin.py ~/plugins/star-writing-skills
codex plugin add star-writing-skills@personal
```

The scaffold command creates the default personal marketplace entry and the
expected `~/plugins/star-writing-skills` location. The copy then replaces the
temporary scaffold with this plugin.

For an existing personal installation, copy the updated source, then use the
official cachebuster and reinstall flow from the same `plugin-creator` root:

```bash
cp -a /absolute/path/to/star-writing-skills/. ~/plugins/star-writing-skills/
python3 scripts/update_plugin_cachebuster.py ~/plugins/star-writing-skills
codex plugin add star-writing-skills@personal
```

Start a new Codex thread after installation or reinstall so the updated skills
are loaded.

## Use

Codex may route automatically, or a request may name a skill explicitly:

```text
Use $star-writing-skills:star-writing to plan an end-to-end manuscript revision.
```

```text
Use $star-writing-skills:star-writing-literature to verify whether each
citation supports its exact clause. Review only.
```

```text
Use $star-writing-skills:star-writing-polish to tighten this passage without
changing claims, numbers, citations, notation, or technical terminology.
Return revised text only.
```

State the manuscript snapshot, permitted scope, locked text, concurrent
writers, and provisional evidence whenever they affect the task.

## Validate

From the plugin root, run:

```bash
python3 scripts/validate_plugin_suite.py
python3 /path/to/plugin-creator/scripts/validate_plugin.py .
```

The bundled validator checks structure, links, portability, routing targets,
and the specifications in `evals/cases.json`. It does not execute an agent or
prove behavioral quality. Forward-test consequential changes in a clean
context before release.
