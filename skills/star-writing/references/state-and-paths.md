# State and Path Policy

Persistent state is optional. Every STAR Writing skill must remain usable from
the supplied materials and current task context without creating a configuration
directory or state file.

## Separate path classes

- **Bundled resources** are immutable files shipped with the plugin. Resolve
  their relative links from the active `SKILL.md`, not from the process working
  directory.
- **Project artifacts** are manuscripts, code, data, figures, and evidence
  supplied for the current research task. Preserve their existing locations.
- **Project state** records current contracts and decisions under
  `.star-writing/` at the resolved project root.
- **User state** contains confirmed preferences intended to apply across
  projects. It must never contain project facts or scientific evidence.

## Resolve the project root

Use this order:

1. Use the root explicitly named by the user or task.
2. Otherwise, use the manuscript directory when it contains the canonical
   entrypoint and its paper-specific sources or artifacts.
3. Otherwise, use the nearest ancestor that already contains `.star-writing/`.
4. Otherwise, use the innermost version-control root that owns the canonical
   artifact and matches the authorized scope.
5. If ownership remains ambiguous, keep state in the current task context. Ask
   for a root only when persistence is materially useful.

Do not infer the project root solely from the agent's launch directory. In a
nested repository, submodule, or worktree, bind manuscript-specific state to
the paper source directory when it is a coherent unit; otherwise use the
innermost repository that owns the canonical artifact. An explicit user choice
overrides both.

Project-local state paths are:

```text
.star-writing/paper-contract.md
.star-writing/terminology-and-symbols.md
.star-writing/decision-log.md
.star-writing/author-style-profile.md
.star-writing/submission-overlays/<target>-<cycle>-<category>-<stage>.md
```

An existing overlay without a stage suffix may be read as a legacy source, but
must not be reused or overwritten until its publication stage and current rules
have been verified.

Interpret these paths relative to the resolved project root. A read-only task
never authorizes state changes. An authorized full-manuscript or multi-section
drafting or revision task permits creation or refresh of the terminology and
symbol ledger when it is needed to keep the requested work consistent and the
root is unambiguous; announce that action. Require explicit authorization for
other persistent state changes.

## Discover a cross-project author profile

Use the first existing profile in this order:

1. a path explicitly supplied for the current task;
2. the project-local `.star-writing/author-style-profile.md`;
3. the file named by `STAR_WRITING_PROFILE`;
4. the platform user-configuration location:
   - POSIX: `${XDG_CONFIG_HOME:-$HOME/.config}/star-writing/author-style-profile.md`;
   - macOS without `XDG_CONFIG_HOME`:
     `$HOME/Library/Application Support/star-writing/author-style-profile.md`;
   - Windows: `%APPDATA%\star-writing\author-style-profile.md`.

Skip an unset environment variable or nonexistent file without error. Do not
search the filesystem broadly, invent another location, or create a profile
merely because none exists. Explicit task instructions override the project
profile, which overrides the cross-project profile, which overrides the bundled
template.

## Preserve portability and boundaries

- Do not put machine-specific absolute paths in bundled skills or templates.
- Prefer project-relative paths in working contracts. Record an external
  absolute path only when it is necessary to identify the responsible source.
- Resolve paths for comparison, but preserve the user's original path spelling
  in reports unless normalization is requested.
- Do not move, duplicate, or rewrite source artifacts to fit the state layout.
- Do not store credentials, tokens, personal identifiers, or submission secrets
  in writing-state files.
- Before writing state, reread the existing file and respect concurrent edits.
