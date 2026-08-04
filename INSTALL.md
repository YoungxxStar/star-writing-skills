# Installing STAR Writing Skills

This document defines the supported personal Codex-plugin installation and
update workflow. It is written for an agent with terminal access, but every
command remains reviewable and can be run manually.

Read this file completely before changing local state. Installation does not
authorize source edits, Git history changes, publication, or modification of
unrelated plugins.

## Recommended agent handoff

```text
Install or update STAR Writing Skills from
https://github.com/YoungxxStar/star-writing-skills

Read INSTALL.md completely. Begin with a read-only preflight and show me the
exact source revision, existing installation, marketplace, staging target,
planned writes and deletions, and validation plan. Ask before performing those
writes.

After approval, follow only the applicable first-install or update path. Use
Codex's bundled plugin-creator workflow, validate the exact source revision and
the staged bundle, and report the resulting versions and paths. Do not modify
the development checkout, hand-edit marketplace files or generated caches, use
force, change unrelated plugins, or commit, push, tag, publish, or release.
```

If only a remote URL is supplied, fetching or cloning it is a filesystem and
network write. Resolve the destination and obtain approval before cloning.

## Supported environment

The commands below target the default personal local-plugin workflow in one
continuous Bash session on a POSIX-like system with:

- Codex CLI and its bundled `plugin-creator` skill;
- Bash, Git, Python 3, `tar`, and `rsync`;
- a local Git checkout of this repository;
- access to the default personal marketplace at
  `~/.agents/plugins/marketplace.json`.

Variables such as `star_source`, `star_commit`, and `star_archive_root` are
shared by later blocks. If the shell session ends, stop and repeat preflight;
do not reconstruct their values from memory. Do not reuse these shell blocks
unchanged on Windows. Use a separately checked equivalent flow. Do not install
the skills independently with a skill installer; STAR Writing Skills is one
plugin bundle.

## Keep five locations distinct

| Location | Role | Mutation rule |
|---|---|---|
| Canonical Git checkout | Maintained source and base semantic version | Read-only during installation |
| Temporary archive | Exact commit selected for installation | May be created and validated for this operation |
| `~/plugins/star-writing-skills` | Personal-marketplace staging copy | May be synchronized only after target review and approval |
| `~/.agents/plugins/marketplace.json` | Personal marketplace registry | Use `plugin-creator`; never hand-edit during this flow |
| Codex-generated cache and configuration | Installed runtime material | Use Codex plugin commands; never copy into or patch directly |

The development checkout, staging copy, and generated cache are not
interchangeable. A cachebuster belongs only to the staging copy. The canonical
manifest retains the base semantic version.

## Phase 1: read-only preflight

Before any clone, scaffold, synchronization, cachebuster, marketplace, or
plugin-install command:

1. Resolve the canonical checkout rather than assuming the current directory.
2. Locate the enabled `plugin-creator` skill root and verify that its scaffold,
   validator, cachebuster, and marketplace-name helpers exist.
3. Check required commands: `git`, `python3`, `tar`, `rsync`, and `codex`.
4. Require a clean source checkout. If tracked or untracked changes exist,
   stop. Do not commit, stash, discard, or silently exclude them.
5. Resolve `HEAD^{commit}` to a full 40-character commit SHA. A branch or tag
   name is not the installation receipt.
6. Read `.codex-plugin/plugin.json` and require
   `name = star-writing-skills` plus a nonempty version.
7. Inspect the expected staging directory, personal marketplace entry, and
   `codex plugin list` output. Classify the operation as a first installation
   or an update.
8. Reject an unexpected target, a symlinked staging directory, a nonlocal
   marketplace entry, a source–target overlap, or an identity mismatch.
9. Report the selected commit, source version, marketplace, staging target,
   existing installed version, planned writes and deletions, and validation
   commands. Obtain approval before proceeding.

A useful read-only source check is:

```bash
set -euo pipefail
star_source="/absolute/path/to/star-writing-skills"
star_creator_root="/absolute/path/to/codex/plugin-creator"

star_source="$(git -C "$star_source" rev-parse --show-toplevel)"
test -e "$star_source/.git"
test -z "$(git -C "$star_source" status --porcelain=v1 --untracked-files=all)"
star_commit="$(git -C "$star_source" rev-parse --verify 'HEAD^{commit}')"
case "$star_commit" in
  "" | *[!0-9a-f]* ) echo "invalid full commit identity" >&2; exit 1 ;;
esac
test "${#star_commit}" -eq 40
test -f "$star_source/.codex-plugin/plugin.json"
test -f "$star_creator_root/SKILL.md"
test -f "$star_creator_root/scripts/create_basic_plugin.py"
test -f "$star_creator_root/scripts/validate_plugin.py"
test -f "$star_creator_root/scripts/update_plugin_cachebuster.py"
test -f "$star_creator_root/scripts/read_marketplace_name.py"
python3 - "$star_source/.codex-plugin/plugin.json" <<'PY'
import json
import sys
from pathlib import Path

manifest = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
assert manifest.get("name") == "star-writing-skills"
assert isinstance(manifest.get("version"), str) and manifest["version"]
print(manifest["name"], manifest["version"])
PY

star_marketplace_json="$(python3 - <<'PY'
from pathlib import Path
print(Path.home() / ".agents" / "plugins" / "marketplace.json")
PY
)"
python3 - "$star_marketplace_json" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
if not path.exists():
    print("personal marketplace: absent")
    raise SystemExit(0)
payload = json.loads(path.read_text(encoding="utf-8"))
entries = [
    item for item in payload.get("plugins", [])
    if item.get("name") == "star-writing-skills"
]
if len(entries) > 1:
    raise SystemExit("duplicate star-writing-skills marketplace entries")
if not entries:
    print("star-writing-skills marketplace entry: absent")
    raise SystemExit(0)
source = entries[0].get("source", {})
if source.get("source") != "local":
    raise SystemExit("star-writing-skills marketplace entry is not local")
if source.get("path") != "./plugins/star-writing-skills":
    raise SystemExit("star-writing-skills marketplace source path is unexpected")
print("star-writing-skills marketplace entry: expected local source")
PY
```

The shell pattern and length check together require a lowercase full SHA. The
agent should also report it rather than treating successful commands as an
implicit receipt.

## Phase 2: validate the exact source revision

Run the repository checks against the clean checkout selected above:

```bash
python3 "$star_source/scripts/validate_plugin_suite.py"
python3 "$star_creator_root/scripts/validate_plugin.py" "$star_source"
```

Recheck the source identity immediately before materializing the exact commit,
not the mutable working directory:

```bash
test -z "$(git -C "$star_source" status --porcelain=v1 --untracked-files=all)"
test "$(git -C "$star_source" rev-parse --verify 'HEAD^{commit}')" = \
  "$star_commit"

star_archive_root="$(mktemp -d)"
git -C "$star_source" archive --format=tar "$star_commit" \
  | tar -xf - -C "$star_archive_root"

python3 "$star_creator_root/scripts/validate_plugin.py" "$star_archive_root"
```

Record `star_archive_root`. Remove it only after confirming that it is the
temporary directory created by this operation and that rollback or inspection
no longer needs it. Never use an unresolved variable or broad home directory as
a deletion target.

The complete suite and regression tests run only in the clean Git checkout,
because source-identity checks require its Git objects. Generated archives and
staging copies receive the official structural plugin validation. These checks
do not prove writing quality or execute a complete agent evaluation.

## Phase 3A: first installation

Use this branch only when both the personal staging directory and its
marketplace entry are absent.

From the `plugin-creator` skill root, create the default personal entry:

```bash
python3 "$star_creator_root/scripts/create_basic_plugin.py" \
  star-writing-skills --with-marketplace
```

Do not use `--force`. The default personal marketplace is discovered
implicitly; do not run `codex plugin marketplace add` for
`~/.agents/plugins/marketplace.json`.

If the staging path exists while the marketplace entry does not, or the entry
exists but points elsewhere, stop and reconcile the state. Do not classify a
partial installation as a safe first install.

## Phase 3B: update an existing installation

Use this branch only when the existing marketplace entry is local and resolves
to the expected `~/plugins/star-writing-skills` staging copy.

- Do not scaffold again.
- Do not hand-edit the marketplace file.
- Inspect the current staged manifest and report its version.
- Use `codex plugin list` if more than one marketplace could surface the plugin.
- Stop if the selected marketplace is remote, the entry points to another
  source, or the staging identity is not `star-writing-skills`.

A previous `+codex.*` suffix is expected in an installed staging version. It is
not a source semantic-version change.

## Phase 4: prepare, preview, and synchronize the staging copy

Create a second temporary copy, add the cachebuster there, and validate it
before touching the fixed staging path:

```bash
star_prepared_root="$(mktemp -d)"
rsync --archive "$star_archive_root/" "$star_prepared_root/"
python3 "$star_creator_root/scripts/update_plugin_cachebuster.py" \
  "$star_prepared_root"
python3 "$star_creator_root/scripts/validate_plugin.py" "$star_prepared_root"
```

Resolve and guard the target before using `rsync --delete`. The guard is a
function because it must be rerun after approval:

```bash
star_plugin_parent="$(python3 - <<'PY'
from pathlib import Path
print(Path.home() / "plugins")
PY
)"
star_plugin_root="$star_plugin_parent/star-writing-skills"

test -d "$star_plugin_parent"
test -d "$star_plugin_root"

star_guard_paths() {
  test ! -L "$star_plugin_parent"
  test ! -L "$star_plugin_root"
  python3 - \
    "$star_source" \
    "$star_archive_root" \
    "$star_prepared_root" \
    "$star_plugin_parent" \
    "$star_plugin_root" <<'PY'
import json
import sys
from pathlib import Path

source = Path(sys.argv[1]).resolve(strict=True)
archive = Path(sys.argv[2]).resolve(strict=True)
prepared = Path(sys.argv[3]).resolve(strict=True)
parent = Path(sys.argv[4]).resolve(strict=True)
target = Path(sys.argv[5]).resolve(strict=True)
expected_parent = (Path.home() / "plugins").resolve(strict=True)
expected_target = (Path.home() / "plugins" / "star-writing-skills").resolve(strict=True)
marketplace_root = (Path.home() / ".agents" / "plugins").resolve(strict=True)
if parent != expected_parent or target.parent != parent:
    raise SystemExit(f"refusing unexpected staging parent: {parent}")
if target != expected_target or target.name != "star-writing-skills":
    raise SystemExit(f"refusing unexpected staging target: {target}")
if target == marketplace_root or marketplace_root in target.parents:
    raise SystemExit("staging target overlaps the marketplace root")
for label, root in (("source", source), ("archive", archive), ("prepared", prepared)):
    if root == target or root in target.parents or target in root.parents:
        raise SystemExit(f"{label} and staging target overlap")
for label, root in (("archive", archive), ("prepared", prepared), ("staging", target)):
    manifest = root / ".codex-plugin" / "plugin.json"
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    if payload.get("name") != "star-writing-skills":
        raise SystemExit(f"{label} has the wrong plugin identity")
PY
}

star_guard_paths
star_rsync_preview="$(
  rsync --archive --delete --dry-run --itemize-changes \
    "$star_prepared_root/" "$star_plugin_root/"
)"
printf '%s\n' "$star_rsync_preview"
```

Show the dry-run output, especially every deletion, and obtain confirmation.
Immediately after confirmation, rerun both the guard and the preview. Continue
only if the complete itemized output is unchanged:

```bash
star_guard_paths
star_rsync_recheck="$(
  rsync --archive --delete --dry-run --itemize-changes \
    "$star_prepared_root/" "$star_plugin_root/"
)"
test "$star_rsync_recheck" = "$star_rsync_preview"
rsync --archive --delete "$star_prepared_root/" "$star_plugin_root/"
python3 "$star_creator_root/scripts/validate_plugin.py" "$star_plugin_root"
```

The `--delete` scope must remain the exact guarded staging directory. Never
substitute a workspace root, home directory, unresolved variable, glob, or
generated cache. If synchronization or validation fails, do not run the Codex
install command. Treat the fixed staging copy as incomplete, retain the
validated prepared copy, and repeat preflight and the approved preview before
repairing it. Do not retry with `--force`.

## Phase 5: install through the marketplace

The staged bundle already contains the helper-generated cachebuster. Read the
actual marketplace name and install through Codex:

```bash
star_marketplace="$(
  python3 "$star_creator_root/scripts/read_marketplace_name.py"
)"
test -n "$star_marketplace"
codex plugin add "star-writing-skills@$star_marketplace"
```

For a separately configured nondefault local marketplace, pass its actual JSON
path to `read_marketplace_name.py` and ensure the marketplace is configured
before adding the plugin. `codex plugin marketplace add` is only for that
explicit nondefault case.

Start a new Codex thread after installation or update. A loaded thread retains
its previous skill snapshot.

## Installation receipt

Report all of the following:

- canonical source path or remote and full commit SHA;
- source manifest version;
- temporary archive validation result;
- staging path and cachebuster version;
- marketplace name and whether this was a first install or update;
- Codex plugin command result;
- any skipped check, warning, or retained temporary directory;
- the requirement to test in a new thread.

Do not describe a source commit as installed unless its validated archive was
the source of the cachebusted prepared bundle that was synchronized and
validated.

## Rollback

Rollback is a new installation operation. Prepare a separate clean checkout
whose `HEAD` is the selected previous commit; do not move or modify the active
development checkout.

1. resolve and report the separate checkout's full `HEAD^{commit}`;
2. repeat preflight and exact-revision validation;
3. preview the staging synchronization and obtain approval;
4. stage the older revision, replace its cachebuster, and reinstall through the
   marketplace;
5. start a new thread and report the rollback receipt.

Never roll back by patching or deleting a generated Codex cache.

## Stop conditions

Stop and ask for resolution when:

- the canonical source is dirty or its exact revision cannot be resolved;
- source, archive, staging, marketplace, and generated cache cannot be
  distinguished;
- the staging path is a symlink or outside the expected personal-plugin root;
- during an update, the marketplace entry is missing, duplicated, remote, or
  points elsewhere;
- during a first install, staging or marketplace state is only partially
  present;
- manifest identity or version is missing or inconsistent;
- required tools or validators are unavailable;
- the dry run contains unexpected writes or deletions;
- validation fails or files change after validation;
- authorization for the next state-changing phase is absent.

Do not repair these conditions with `--force`, an automatic commit, stash,
discard, marketplace edit, or direct cache mutation.
