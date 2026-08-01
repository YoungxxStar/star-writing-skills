#!/usr/bin/env python3
"""Validate the STAR Writing Skills plugin as one coherent suite.

Interface
---------
Run with no arguments from any directory:

    python3 scripts/validate_plugin_suite.py

The script locates the plugin root from its own path and validates the manifest,
skill frontmatter, UI metadata, relative Markdown links, reference structure,
path portability, and behavioral evaluation specifications. It uses only the
Python standard library and does not modify the plugin.

Implementation
--------------
This validator complements Codex's official plugin and skill validators. It
checks cross-skill contracts that those structural validators do not cover,
especially whether evaluation routes name skills that actually exist. It does
not execute an agent or establish behavioral correctness.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / ".codex-plugin" / "plugin.json"
SKILLS_DIR = ROOT / "skills"
EVALS = ROOT / "evals" / "cases.json"

REQUIRED_EVAL_FIELDS = {
    "id",
    "prompt",
    "expected_controller",
    "expected_mode",
    "must",
    "must_not",
}
ALLOWED_MODES = {
    "explore",
    "converge",
    "audit",
    "detect",
    "plan",
    "draft",
    "revise",
    "polish",
    "rewrite",
    "edit",
    "submit",
}
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
PORTABLE_TEXT_SUFFIXES = {".json", ".md", ".py", ".txt", ".yaml", ".yml"}
MACHINE_SPECIFIC_PATHS = {
    "HPC or workspace path": re.compile(r"/(?:cephfs|scratch|workspaces)/"),
    "literal POSIX user home": re.compile(
        r"/(?:home|users|Users)/[^/\s`'\"]+/"
    ),
    "literal Windows user home": re.compile(
        r"[A-Za-z]:\\Users\\[^\\\s`'\"]+\\"
    ),
}


def load_json(path: Path, errors: list[str]) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"missing file: {path.relative_to(ROOT)}")
    except json.JSONDecodeError as exc:
        errors.append(
            f"invalid JSON in {path.relative_to(ROOT)}: "
            f"line {exc.lineno}, column {exc.colno}: {exc.msg}"
        )
    return None


def parse_frontmatter(path: Path, errors: list[str]) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        errors.append(f"missing YAML frontmatter: {path.relative_to(ROOT)}")
        return {}

    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        errors.append(f"unterminated YAML frontmatter: {path.relative_to(ROOT)}")
        return {}

    metadata: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip("\"'")
    return metadata


def validate_manifest(errors: list[str]) -> None:
    manifest = load_json(MANIFEST, errors)
    if not isinstance(manifest, dict):
        return

    name = manifest.get("name")
    version = manifest.get("version")
    valid_root_names = {value for value in (name, version) if isinstance(value, str)}
    if ROOT.name not in valid_root_names:
        errors.append(
            f"plugin directory {ROOT.name!r} matches neither manifest name "
            f"{name!r} nor version {version!r}"
        )
    if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9-]+", name):
        errors.append(f"invalid manifest name: {name!r}")
    if not isinstance(version, str) or not version.strip():
        errors.append(f"invalid manifest version: {version!r}")
    if manifest.get("skills") != "./skills/":
        errors.append("manifest skills path must be './skills/'")

    interface = manifest.get("interface")
    if not isinstance(interface, dict):
        errors.append("manifest interface must be an object")
        return

    prompts = interface.get("defaultPrompt")
    if not isinstance(prompts, list):
        errors.append("manifest interface.defaultPrompt must be a list")
    else:
        if not 1 <= len(prompts) <= 3:
            errors.append("manifest interface.defaultPrompt must contain 1 to 3 prompts")
        for index, prompt in enumerate(prompts, start=1):
            if not isinstance(prompt, str) or not prompt.strip():
                errors.append(f"manifest default prompt #{index} must be a non-empty string")
            elif len(prompt) > 128:
                errors.append(f"manifest default prompt #{index} exceeds 128 characters")


def validate_skills(errors: list[str]) -> set[str]:
    skill_files = sorted(SKILLS_DIR.glob("*/SKILL.md"))
    if not skill_files:
        errors.append("no skills/*/SKILL.md files found")
        return set()

    names: set[str] = set()
    for skill_file in skill_files:
        relative = skill_file.relative_to(ROOT)
        metadata = parse_frontmatter(skill_file, errors)
        name = metadata.get("name", "")
        description = metadata.get("description", "")

        if not name:
            errors.append(f"missing skill name: {relative}")
        elif name != skill_file.parent.name:
            errors.append(
                f"skill name {name!r} does not match directory "
                f"{skill_file.parent.name!r}: {relative}"
            )
        elif name in names:
            errors.append(f"duplicate skill name: {name}")
        else:
            names.add(name)

        if not description:
            errors.append(f"missing skill description: {relative}")

        extra_fields = sorted(set(metadata) - {"name", "description"})
        if extra_fields:
            errors.append(
                f"unsupported frontmatter fields in {relative}: "
                f"{', '.join(extra_fields)}"
            )

        line_count = len(skill_file.read_text(encoding="utf-8").splitlines())
        if line_count > 500:
            errors.append(f"SKILL.md exceeds 500 lines ({line_count}): {relative}")

        agent_file = skill_file.parent / "agents" / "openai.yaml"
        if not agent_file.is_file():
            errors.append(f"missing UI metadata: {agent_file.relative_to(ROOT)}")
            continue
        agent_text = agent_file.read_text(encoding="utf-8")
        for field in ("display_name:", "short_description:", "default_prompt:"):
            if field not in agent_text:
                errors.append(
                    f"missing {field[:-1]} in {agent_file.relative_to(ROOT)}"
                )
        if name and f"${name}" not in agent_text:
            errors.append(
                f"default prompt does not mention ${name}: "
                f"{agent_file.relative_to(ROOT)}"
            )

    return names


def validate_reference_structure(errors: list[str]) -> None:
    for path in sorted(SKILLS_DIR.glob("*/references/**/*")):
        if not path.is_file():
            continue
        relative = path.relative_to(ROOT)
        if path.parent.name != "references":
            errors.append(f"nested reference file is not allowed: {relative}")
            continue

        lines = path.read_text(encoding="utf-8").splitlines()
        if len(lines) > 100 and "## Contents" not in lines[:30]:
            errors.append(
                f"reference over 100 lines lacks a top-level Contents section: "
                f"{relative}"
            )

        skill_file = path.parent.parent / "SKILL.md"
        skill_text = skill_file.read_text(encoding="utf-8")
        expected_link = f"references/{path.name}"
        if expected_link not in skill_text:
            errors.append(
                f"reference is not linked directly from its SKILL.md: {relative}"
            )


def validate_markdown_links(errors: list[str]) -> None:
    for path in sorted(ROOT.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        for match in MARKDOWN_LINK.finditer(text):
            raw_target = match.group(1).strip()
            if not raw_target or raw_target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            if " " in raw_target and not raw_target.startswith("<"):
                raw_target = raw_target.split(maxsplit=1)[0]
            target = raw_target.strip("<>").split("#", 1)[0]
            if not target:
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                errors.append(
                    f"broken Markdown link in {path.relative_to(ROOT)}: {target}"
                )


def validate_path_portability(errors: list[str]) -> None:
    validator = Path(__file__).resolve()
    for path in sorted(ROOT.rglob("*")):
        if (
            not path.is_file()
            or path.resolve() == validator
            or path.suffix not in PORTABLE_TEXT_SUFFIXES
        ):
            continue
        text = path.read_text(encoding="utf-8")
        for label, pattern in MACHINE_SPECIFIC_PATHS.items():
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                errors.append(
                    f"{label} in {path.relative_to(ROOT)}:{line}: "
                    f"{match.group(0)}"
                )


def validate_eval_specs(skill_names: set[str], errors: list[str]) -> int:
    cases = load_json(EVALS, errors)
    if not isinstance(cases, list):
        if cases is not None:
            errors.append("evals/cases.json must contain a JSON array")
        return 0

    seen_ids: set[str] = set()
    for index, case in enumerate(cases):
        label = f"eval case #{index + 1}"
        if not isinstance(case, dict):
            errors.append(f"{label} must be an object")
            continue

        missing = REQUIRED_EVAL_FIELDS - case.keys()
        if missing:
            errors.append(f"{label} missing fields: {', '.join(sorted(missing))}")

        prompt = case.get("prompt")
        if not isinstance(prompt, str) or not prompt.strip():
            errors.append(f"{label} has an invalid prompt")

        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id.strip():
            errors.append(f"{label} has an invalid id")
        elif case_id in seen_ids:
            errors.append(f"duplicate eval id: {case_id}")
        else:
            seen_ids.add(case_id)
            label = f"eval {case_id}"

        controller = case.get("expected_controller")
        if controller not in skill_names:
            errors.append(f"{label} names unknown controller: {controller!r}")

        mode = case.get("expected_mode")
        if mode not in ALLOWED_MODES:
            errors.append(f"{label} has unsupported mode: {mode!r}")

        routes = case.get("expected_routes", [])
        if not isinstance(routes, list):
            errors.append(f"{label} expected_routes must be a list")
        else:
            unknown = sorted(set(routes) - skill_names)
            if unknown:
                errors.append(
                    f"{label} names unknown routes: {', '.join(unknown)}"
                )

        for field in ("must", "must_not"):
            values = case.get(field)
            if (
                not isinstance(values, list)
                or not values
                or not all(isinstance(value, str) and value.strip() for value in values)
            ):
                errors.append(f"{label} field {field} must be a non-empty string list")

        must = case.get("must", [])
        must_not = case.get("must_not", [])
        if isinstance(must, list) and isinstance(must_not, list):
            overlap = sorted(set(must) & set(must_not))
            if overlap:
                errors.append(
                    f"{label} has contradictory must and must_not entries: "
                    f"{', '.join(overlap)}"
                )

    return len(cases)


def main() -> int:
    errors: list[str] = []
    validate_manifest(errors)
    skill_names = validate_skills(errors)
    validate_reference_structure(errors)
    validate_markdown_links(errors)
    validate_path_portability(errors)
    spec_count = validate_eval_specs(skill_names, errors)

    if errors:
        print("STAR Writing Skills plugin-suite validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "STAR Writing Skills plugin-suite validation passed: "
        f"{len(skill_names)} skills, {spec_count} behavioral specifications "
        "structurally valid, all local Markdown links resolved, no "
        "machine-specific paths detected. "
        "No behavioral executions were performed."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
