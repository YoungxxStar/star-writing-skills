# STAR Writing Skills

STAR Writing Skills is a cross-disciplinary, cross-language Codex plugin for
building defensible research papers and their associated supplements,
rebuttals, and release artifacts. It coordinates framing, literature, methods,
evidence, drafting, polishing, review, live submission checks, and
evidence-driven workflow evolution without
binding the workflow to a research field, project, language, venue, or fixed
paper template.

## Architecture

The plugin contains one paper router, eight focused paper skills, and one
maintenance skill.

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
| `star-writing-evolve` | Feedback reconstruction, learning-scope decisions, authorized skill evolution, and regression validation |

Use the paper router for work spanning several paper stages. Use a focused
paper skill when one owner clearly controls the requested deliverable. Use
`star-writing-evolve` only for explicit maintenance of this plugin's reusable
behavior; it is not another manuscript stage.

## Working model

Use only the stages the task needs:

`Orient -> Contract -> [Ground <-> Explore] -> Converge -> Structure -> Write -> Audit -> Handoff`

Exploration uses current research, data, and records to generate alternatives;
each consequential uncertainty returns to targeted grounding. Convergence tests
the surviving accounts against the closest work and available evidence before
drafting. Submission is a live, target-specific audit layered onto a stable
paper and its associated artifacts.

The suite is dynamic but not self-modifying by default. Praise, correction,
friction, failure, and self-discovered methods can become evolution candidates.
Persistent skill behavior changes only after the episode is reconstructed, the
lesson is placed at the narrowest valid layer, conflicts are checked, and the
user explicitly authorizes the identified source update. Commit, installation,
push, marketplace update, and release remain separate actions.

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
- evolve changes an identified skill-development source only within explicitly
  authorized scope and never implies installation, push, publication, or paper
  edits.

## Install

Install the plugin as one bundle. Do not copy the ten skills separately or
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

```text
Use $star-writing-skills:star-writing-evolve to audit whether this accepted
workflow should become a reusable skill rule. Do not modify source yet.
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
