# Repository Guide for Agents and Contributors

This file applies to the entire STAR Writing Skills repository. It keeps the
implemented plugin, public documentation, tests, release metadata, and local
installation procedure aligned.

## Work from the canonical source

- Treat this Git checkout as the only development source. Do not edit an
  installed plugin cache or generated marketplace copy.
- Inspect the worktree before editing and preserve unrelated user changes.
- Read a changed skill's complete `SKILL.md` and the governing references it
  links before changing its behavior.
- Keep manuscripts, credentials, private evidence, machine-specific paths,
  generated caches, and build artifacts out of the repository.

## Keep public documents synchronized

Review the following matrix for every change. Update a document when the
condition in its row applies; do not churn unaffected files.

| Document | Update when |
|---|---|
| `README.md` | A public capability, skill count, skill route, user workflow, example, limitation, or validation command changes |
| `AGENTS.md` | Repository-wide ownership, editing, validation, documentation, Git, or installation expectations change |
| `CHANGELOG.md` | A versioned public capability, compatibility boundary, or release milestone is introduced |
| `CONTRIBUTING.md` | Contributor scope, evidence, testing, review, or pull-request expectations change |
| `INSTALL.md` | Installation, update, rollback, marketplace, cache, or verification behavior changes |
| `.codex-plugin/plugin.json` | Plugin identity, version, public description, capability, or default prompt changes |

When a skill is added, removed, renamed, or rerouted, review the router,
manifest, README skill map, evaluation cases, and suite validator together.
When the manifest version changes, ensure the current milestone is recorded in
`CHANGELOG.md`. Markdown links must remain relative and resolvable.

## Preserve skill contracts

- Keep each behavior owned by one skill with a distinct trigger,
  responsibility, and output contract.
- Preserve the boundary between read-only audit, derived-artifact creation,
  manuscript edits, project-state writes, plugin-source changes, Git actions,
  installation, and publication.
- Do not treat author approval as scientific evidence or reusable skill
  evidence. Generic evolution is governed by STAR HotSkills, not by a hidden
  store in this repository.
- Update the router only when routing behavior actually changes.

For Diff2PS specifically, preserve all of these invariants:

- bind exact before and after identities before interpretation;
- build a complete textual-diff candidate ledger;
- classify every hunk and every non-empty changed line;
- keep gray `[before]` and red `[after]` excerpts source-verbatim;
- keep blue `[psN]` text interpretive and sequential in document order;
- record exact, meaning-preserving exclusions such as reflow rather than
  silently omitting them;
- leave both inputs and unrelated project files unchanged.

## Validate proportionally

Run from the repository root:

```bash
python3 scripts/validate_plugin_suite.py
python3 <plugin-creator-root>/scripts/validate_plugin.py .
git diff --check
```

Also run the focused validator and positive/negative behavioral cases for the
changed owner. Structural validation is necessary but does not establish
writing quality. For rendered artifacts, inspect representative early, middle,
late, and dense-change pages and bind the report to the exact artifact.

Before handoff, verify that local Markdown links resolve, the README skill map
matches the installed skill directories, the manifest version has a CHANGELOG
entry, and no private or machine-specific content was introduced.

## Keep Git and installation actions explicit

- Stage only reviewed files; exclude generated caches and temporary outputs.
- Use a focused branch for repository changes when starting from the default
  branch.
- Treat commit, push, tag, release, installation, marketplace refresh, and
  cache cleanup as separate actions requiring their applicable authorization.
- Follow [INSTALL.md](INSTALL.md) for installation or local refresh. Validate
  the exact source revision before staging it, and report the installed commit
  and manifest version afterward.
