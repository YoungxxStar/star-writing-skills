# STAR Writing Skills

STAR Writing Skills is a cross-disciplinary, cross-language Codex plugin for
building defensible research papers and their associated supplements,
rebuttals, and release artifacts. It coordinates framing, literature, methods,
evidence, drafting, polishing, review, live submission checks, and
an interactive project Writing Ledger, together with evidence-driven workflow
evolution, without
binding the workflow to a research field, project, language, venue, or fixed
paper template.

## Architecture

The plugin contains one paper router, ten focused paper skills, and one
maintenance skill.

| Skill | Owner of |
|---|---|
| `star-writing` | Multi-stage coordination and paper-wide or cross-artifact requests |
| `star-writing-start` | Read-only onboarding, canonical snapshot discovery, Paper Map construction, and next-step routing |
| `star-writing-ledger` | One-decision-at-a-time control of core propositions, concepts, canonical terms, names, acronyms, labels, and symbols |
| `star-writing-frame` | First-principles motivation, problem formulation, novelty, and argument spine |
| `star-writing-literature` | Closest work, citation support, and positioning |
| `star-writing-method` | Information availability, notation, equations, procedures, and implementation alignment |
| `star-writing-evidence` | Study design, metrics, statistics, results, figures, tables, and claim-evidence alignment |
| `star-writing-draft` | Drafting, restructuring, and paper-type-appropriate evidence allocation |
| `star-writing-polish` | Meaning-preserving language improvement and translation |
| `star-writing-review` | Purpose-specific, adversarial, and consistency review |
| `star-writing-submit` | Live requirements, rendering or forms, identity, and packaging |
| `star-writing-evolve` | Feedback reconstruction, authorized project incubation, canonical promotion decisions, skill evolution, and regression validation |

Use the paper router for work spanning several paper stages. Use a focused
paper skill when one owner clearly controls the requested deliverable. Use
`star-writing-ledger` when a load-bearing proposition, concept, name, term, or
symbol must be established or reconciled across the project. Use
`star-writing-evolve` only for explicit maintenance of this plugin's reusable
behavior; it is not another manuscript stage.

The Project Writing Ledger is one logical contract over
`.star-writing/paper-contract.md`, `.star-writing/terminology-and-symbols.md`,
and `.star-writing/decision-log.md`. It does not create a duplicate aggregate
file. Only accepted, current entries constrain later writing; responsible
scientific sources remain authoritative for facts. Acceptance fixes the
project's chosen meaning or expression, while epistemic status still controls
whether a proposition may be stated as established, bounded, exploratory, or
not supported.

## Working model

Use only the stages the task needs:

`Orient -> Contract/Ledger -> [Ground <-> Explore] -> Converge -> Structure -> Write -> Audit -> Handoff`

Exploration uses current research, data, and records to generate alternatives;
each consequential uncertainty returns to targeted grounding. Convergence tests
the surviving accounts against the closest work and available evidence before
drafting. Submission is a live, target-specific audit layered onto a stable
paper and its associated artifacts.

The suite is dynamic but not self-modifying by default. Praise, correction,
friction, failure, and self-discovered methods are possible signals, not
automatic updates. A review may correctly produce no evolution action.
Candidates remain task-local unless the user authorizes either a named inactive
record in the project's `.star-writing/evolution/` workspace or a distinct,
public-safe record in the development repository's canonical
[promotion ledger](evolution/README.md). Neither record is an active rule or an
authority grant, and neither belongs to the Project Writing Ledger. Persistent
skill behavior changes only after the episode is reconstructed, the lesson is
placed at the narrowest valid layer, matched behavior is evaluated, conflicts
are checked, and the user separately authorizes the identified source update.
Commit, installation, push, marketplace update, and release remain separate
actions.

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
  scientific terminology;
- stage writes only an identified, inactive project-local evolution record
  within explicitly authorized scope;
- evolve writes an identified canonical promotion record or changes active
  skill-development source only within separately authorized scope; record
  persistence never activates behavior, and none of these actions implies
  installation, push, publication, or paper edits.

## Install

Install the plugin as one bundle. Do not copy the twelve skills separately or
hand-edit marketplace JSON.

Clone or download this repository first. For a private GitHub checkout over
SSH, for example:

```bash
git clone git@github.com:YOUR_GITHUB_OWNER/star-writing-skills.git
```

For a first personal installation, create the default marketplace entry and
staging path from Codex's bundled `plugin-creator` skill root:

```bash
python3 scripts/create_basic_plugin.py star-writing-skills --with-marketplace
```

For either a first installation or an update, stage an exact validated commit.
The archive excludes `.git`; the synchronized staging path also removes files
retired by that commit. Set `star_commit` to the validated commit hash, not an
uncommitted working tree:

```bash
set -euo pipefail
star_source="/absolute/path/to/star-writing-skills"
star_commit="VALIDATED_COMMIT_HASH"
star_stage_dir="$(mktemp -d)"
star_plugin_root="$(python3 - <<'PY'
from pathlib import Path
print((Path.home() / "plugins" / "star-writing-skills").resolve())
PY
)"
test "$star_commit" != "VALIDATED_COMMIT_HASH"
git -C "$star_source" archive --format=tar "$star_commit" | tar -xf - -C "$star_stage_dir"
python3 scripts/validate_plugin.py "$star_stage_dir"
python3 - "$star_source" "$star_stage_dir" "$star_plugin_root" <<'PY'
import json
import sys
from pathlib import Path

source = Path(sys.argv[1]).resolve(strict=True)
stage = Path(sys.argv[2]).resolve(strict=True)
target = Path(sys.argv[3]).resolve(strict=True)
expected = (Path.home() / "plugins" / "star-writing-skills").resolve()
if target != expected or target.name != "star-writing-skills":
    raise SystemExit(f"refusing unexpected staging target: {target}")
if source == target or source in target.parents or target in source.parents:
    raise SystemExit("development source and plugin staging must be separate")
if ".codex/plugins/cache" in target.as_posix():
    raise SystemExit("refusing to synchronize into a generated cache")
for label, root in (("archive", stage), ("current target", target)):
    manifest = root / ".codex-plugin" / "plugin.json"
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    if payload.get("name") != "star-writing-skills":
        raise SystemExit(f"{label} has the wrong plugin identity")
PY
rsync --archive --delete "$star_stage_dir/" "$star_plugin_root/"
python3 scripts/validate_plugin.py "$star_plugin_root"
```

The guarded block stops if archive creation, validation, identity checks, or
path checks fail. The `--delete` scope is the resolved personal-plugin staging
directory only; it cannot target the development checkout, marketplace root, or
generated cache. Inspect or remove the temporary directory after use.

Then apply the official cachebuster and reinstall flow from the same
`plugin-creator` root. Read the actual personal-marketplace name rather than
assuming it:

```bash
set -euo pipefail
star_plugin_root="$(python3 - <<'PY'
from pathlib import Path
print((Path.home() / "plugins" / "star-writing-skills").resolve())
PY
)"
python3 scripts/update_plugin_cachebuster.py "$star_plugin_root"
python3 scripts/validate_plugin.py "$star_plugin_root"
star_marketplace="$(python3 scripts/read_marketplace_name.py)"
codex plugin add "star-writing-skills@$star_marketplace"
```

Start a new Codex thread after installation or reinstall so the updated skills
are loaded.

## Use

Codex may route automatically, or a request may name a skill explicitly. These
templates remain neutral to field, language, paper type, project, and venue:

| Skill | Example request |
|---|---|
| `star-writing` | `Use $star-writing-skills:star-writing to coordinate an end-to-end revision of this manuscript. Audit first and do not edit yet.` |
| `star-writing-start` | `Use $star-writing-skills:star-writing-start on this paper or project path. Build a Paper Map and recommend the next step without editing.` |
| `star-writing-ledger` | `Use $star-writing-skills:star-writing-ledger to establish the core propositions, canonical terms, and symbols one decision at a time. Preview only.` |
| `star-writing-frame` | `Use $star-writing-skills:star-writing-frame to test the problem, motivation, and contribution logic from first principles. Review only.` |
| `star-writing-literature` | `Use $star-writing-skills:star-writing-literature to verify the closest work and whether every citation supports its exact clause. Review only.` |
| `star-writing-method` | `Use $star-writing-skills:star-writing-method to audit the information contract, notation, equations, and method-to-practice alignment. Do not edit.` |
| `star-writing-evidence` | `Use $star-writing-skills:star-writing-evidence to map each claim to evidence and assess comparison fairness, measures, and result interpretation. Review only.` |
| `star-writing-draft` | `Use $star-writing-skills:star-writing-draft to draft the Results section from the accepted frame and verified evidence. Return text only.` |
| `star-writing-polish` | `Use $star-writing-skills:star-writing-polish to tighten this passage without changing claims, numbers, citations, notation, or technical terms. Preview changes.` |
| `star-writing-review` | `Use $star-writing-skills:star-writing-review to act as a skeptical reviewer and assess novelty, validity, mechanism, utility, and reproducibility. Do not edit.` |
| `star-writing-submit` | `Use $star-writing-skills:star-writing-submit to check this submission against the live rules of the named venue, cycle, track, and stage, including the rendered artifact and package. Review only.` |
| `star-writing-evolve` | `Use $star-writing-skills:star-writing-evolve to audit whether this accepted workflow contains a reusable lesson. Do not write project state or source yet.` |

Persistent evolution needs a narrower authorization than an audit. For example:

```text
Use $star-writing-skills:star-writing-evolve in stage mode to record this one
project-bounded observation under the resolved project root. Do not modify the
plugin source, commit, install, or push.
```

```text
Use $star-writing-skills:star-writing-evolve to persist this one unresolved,
public-safe workflow candidate in the canonical promotion ledger. Do not change
active rules, commit, install, or push.
```

State the manuscript snapshot, permitted scope, locked text, concurrent
writers, and provisional evidence whenever they affect the task.

## Validate

From the canonical Git development checkout, run:

```bash
python3 scripts/validate_plugin_suite.py
python3 scripts/test_candidate_validator.py
python3 scripts/test_project_evolution_validator.py
python3 /path/to/plugin-creator/scripts/validate_plugin.py .
```

The bundled validator checks structure, links, portability, routing targets,
canonical promotion-ledger schema and privacy guardrails, and the
specifications in `evals/cases.json`. It does not execute an agent or prove
behavioral quality.
Candidate source-identity and revision checks require the checkout's Git
objects; use the official plugin validator alone for a generated archive or
staging copy. The isolated candidate regression exercises positive,
non-activation, privacy, provenance, lifecycle, and revision cases without
modifying the development checkout. The isolated project-state regression
checks that optional `.star-writing/evolution/` records remain scoped,
inactive, untrusted, and isolated from unrelated project files. To validate an
actual project workspace, pass its root explicitly:

```bash
python3 scripts/validate_project_evolution.py --project-root /absolute/project/root
```

Forward-test consequential changes in a clean context before release.

When an authorized candidate reaches validated but uncommitted source, obtain
its exact maintained-source receipt with:

```bash
python3 scripts/validate_plugin_suite.py --print-source-snapshot
```

Candidate records do not enter this digest and never become active source.
