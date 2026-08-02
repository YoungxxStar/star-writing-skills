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
PAPER_MODES = {
    "explore",
    "converge",
    "audit",
    "detect",
    "plan",
    "preview",
    "draft",
    "revise",
    "polish",
    "rewrite",
    "edit",
    "submit",
}
ALLOWED_MODES = PAPER_MODES | {"evolve"}
CONTROLLER_MODES = {
    "star-writing": PAPER_MODES,
    "star-writing-frame": {"explore", "converge", "audit", "revise"},
    "star-writing-literature": {"audit", "revise"},
    "star-writing-method": {"audit", "revise"},
    "star-writing-evidence": {"audit", "plan"},
    "star-writing-draft": {"plan", "draft", "revise"},
    "star-writing-polish": {"detect", "preview", "rewrite", "edit"},
    "star-writing-review": {"audit"},
    "star-writing-submit": {"submit"},
    "star-writing-evolve": {"audit", "plan", "evolve"},
}
PRINCIPLE_TAG_CONSUMERS = {
    "star-writing": "references/principle-tags.md",
    "star-writing-draft": "../star-writing/references/principle-tags.md",
    "star-writing-evidence": "../star-writing/references/principle-tags.md",
    "star-writing-frame": "../star-writing/references/principle-tags.md",
    "star-writing-literature": "../star-writing/references/principle-tags.md",
    "star-writing-method": "../star-writing/references/principle-tags.md",
    "star-writing-polish": "../star-writing/references/principle-tags.md",
    "star-writing-review": "../star-writing/references/principle-tags.md",
    "star-writing-submit": "../star-writing/references/principle-tags.md",
    "star-writing-evolve": "../star-writing/references/principle-tags.md",
}
EVOLUTION_POLICY_CONSUMERS = {
    "star-writing": "references/evolution-policy.md",
    "star-writing-draft": "../star-writing/references/evolution-policy.md",
    "star-writing-evidence": "../star-writing/references/evolution-policy.md",
    "star-writing-evolve": "../star-writing/references/evolution-policy.md",
    "star-writing-frame": "../star-writing/references/evolution-policy.md",
    "star-writing-literature": "../star-writing/references/evolution-policy.md",
    "star-writing-method": "../star-writing/references/evolution-policy.md",
    "star-writing-polish": "../star-writing/references/evolution-policy.md",
    "star-writing-review": "../star-writing/references/evolution-policy.md",
    "star-writing-submit": "../star-writing/references/evolution-policy.md",
}
REQUIRED_GUARDRAIL_EVAL_IDS = {
    "adversarial-rejection-case",
    "objective-two-sided-judgment",
    "first-principles-motivation-convergence",
    "research-grounded-terminology-ledger",
    "approval-gated-tui-revision",
    "sentence-paragraph-confidence-gate",
    "exploration-to-manuscript-promotion",
    "highlighted-principle-rationale",
    "non-english-polish-no-translation",
    "paper-no-forced-supporting-artifact",
    "rebuttal-review-no-rejection-template",
    "paper-submission-applicability-gate",
    "qualitative-non-english-shortening",
}
REQUIRED_GOVERNING_PRINCIPLE_IDS = {
    "PROBLEM-CONTRACT",
    "CONTRACT-ALIGNMENT",
    "RESPONSIBLE-SOURCE",
    "PROPOSITION-SUPPORT",
    "RELATIONAL-NOVELTY",
    "SYMMETRIC-JUDGMENT",
    "CONTEXT-LAYERS",
    "WORKFLOW-DEPENDENCY",
    "INFORMATION-BOUNDARY",
    "RECONSTRUCTABLE-METHOD",
    "CAPABILITY-STAGE",
    "INFERENCE-LAYER",
    "IDENTIFICATION-CEILING",
    "COMPARISON-PARITY",
    "STATISTICAL-CONTRACT",
    "OPERATIONAL-SEMANTICS",
    "GENERALITY-AXES",
    "DECISION-TIMING",
    "REPRODUCTION-LEVEL",
    "SUPPORT-GATE",
    "CONTENT-NECESSITY",
    "INFERENTIAL-ORDER",
    "CORE-COMPLETENESS",
    "TERM-STABILITY",
    "RECOVERABLE-COMPRESSION",
    "SEMANTIC-PRESERVATION",
    "ARTIFACT-FIT",
    "ACCESSIBLE-ENCODING",
    "AUTHORIZED-SCOPE",
    "CURRENT-INTENT",
    "DEPENDENCY-PROPAGATION",
    "ARTIFACT-IDENTITY",
    "AUDIT-COVERAGE",
    "LIVE-REQUIREMENTS",
}
REQUIRED_REASONING_LENS_IDS = {
    "CURRENT-EVIDENCE-FIRST",
    "FIRST-PRINCIPLES",
    "MOTIVATION-AS-STORY",
    "DIVERGENT-THINKING",
    "SELF-CORRECTION",
    "ADVERSARIAL-REVIEW",
    "CONFIDENCE-GATE",
    "LESS-BUT-CORRECT",
}
REQUIRED_EVOLUTION_EVAL_CONTRACTS = {
    "evolution-feedback-scope-triage": {
        "controller": "star-writing-evolve",
        "mode": "audit",
        "routes": {"star-writing-submit"},
        "must": {
            "reconstruct and classify the positive feedback, dissatisfaction, one-time preference, project fact, and venue claim separately",
            "return a candidate decision for every signal without changing persistent source or state",
        },
        "must_not": {
            "infer a universal rule or causal mechanism from praise, silence, one complaint, or one successful output",
            "treat a remembered venue rule as current or store a local signal as a shared skill rule",
        },
    },
    "active-task-evolution-handoff": {
        "controller": "star-writing-evidence",
        "mode": "audit",
        "routes": {"star-writing-evolve"},
        "must": {
            "keep the active evidence controller responsible for the paper deliverable and hand off only a task-local evolution candidate",
            "distinguish a rule defect from execution, information, authority, tool, environment, and project-scope failures using observable evidence",
        },
        "must_not": {
            "silently switch the paper task into evolve mode or modify skill source during the read-only audit",
            "promote a self-discovered method from one successful example",
        },
    },
    "evolution-conflict-authorization-plan": {
        "controller": "star-writing-evolve",
        "mode": "plan",
        "routes": {"star-writing-submit"},
        "must": {
            "resolve authority, factual responsibility, applicability, and scope as separate questions",
            "name the canonical owner, dependent files, positive and negative regressions, version impact, and separate action permissions",
        },
        "must_not": {
            "let authorization turn an unverified scientific or venue claim into fact",
            "edit, commit, install, push, or release in plan mode",
        },
    },
    "authorized-evolution-release-boundary": {
        "controller": "star-writing-evolve",
        "mode": "evolve",
        "routes": set(),
        "must": {
            "bind the approved change to the current canonical source, revision, dirty state, installed-version distinction, and file snapshots",
            "recheck each affected file snapshot immediately before writing and stop on overlapping ownership or semantically rebase only after ownership is resolved",
            "run structural validators and clean-context positive, negative, no-authorization, and regression tests on the exact final source snapshot",
        },
        "must_not": {
            "absorb unrelated changes or treat an installed cache as development source",
            "overwrite, stage, or commit another writer's changes",
            "install, update a cache or marketplace, push, tag, publish, or release without separate explicit authorization",
        },
    },
}
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
SEMVER = re.compile(
    r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$"
)
SHIPPING_PLACEHOLDER = re.compile(
    r"\b(?:TODO|TBD|FIXME|REPLACE_ME)\b|<skill-name>", re.IGNORECASE
)
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
    if not isinstance(version, str) or not SEMVER.fullmatch(version):
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

        shipped_text = skill_file.read_text(encoding="utf-8")
        if SHIPPING_PLACEHOLDER.search(shipped_text):
            errors.append(f"shipping placeholder in {relative}")

        agent_file = skill_file.parent / "agents" / "openai.yaml"
        if not agent_file.is_file():
            errors.append(f"missing UI metadata: {agent_file.relative_to(ROOT)}")
            continue
        agent_text = agent_file.read_text(encoding="utf-8")
        if SHIPPING_PLACEHOLDER.search(agent_text):
            errors.append(f"shipping placeholder in {agent_file.relative_to(ROOT)}")
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


def validate_cross_skill_contracts(
    skill_names: set[str], errors: list[str]
) -> None:
    contract_sets = {
        "controller-mode": set(CONTROLLER_MODES),
        "principle-tag": set(PRINCIPLE_TAG_CONSUMERS),
        "evolution-policy": set(EVOLUTION_POLICY_CONSUMERS),
    }
    for label, contract_names in contract_sets.items():
        missing = sorted(skill_names - contract_names)
        stale = sorted(contract_names - skill_names)
        if missing:
            errors.append(
                f"skills missing from {label} contract: {', '.join(missing)}"
            )
        if stale:
            errors.append(
                f"stale skills in {label} contract: {', '.join(stale)}"
            )

    for skill_name, expected_link in PRINCIPLE_TAG_CONSUMERS.items():
        skill_file = SKILLS_DIR / skill_name / "SKILL.md"
        if not skill_file.is_file():
            errors.append(f"missing skill file for principle contract: {skill_name}")
            continue
        if expected_link not in skill_file.read_text(encoding="utf-8"):
            errors.append(
                f"{skill_name} does not consume the shared principle-tag contract"
            )

    for skill_name, expected_link in EVOLUTION_POLICY_CONSUMERS.items():
        skill_file = SKILLS_DIR / skill_name / "SKILL.md"
        if not skill_file.is_file():
            errors.append(f"missing skill file for evolution contract: {skill_name}")
            continue
        if expected_link not in skill_file.read_text(encoding="utf-8"):
            errors.append(
                f"{skill_name} does not consume the shared evolution policy"
            )

    registry = SKILLS_DIR / "star-writing" / "references" / "principle-tags.md"
    if not registry.is_file():
        errors.append("missing shared principle registry")
        return

    registry_text = registry.read_text(encoding="utf-8")
    for identifier in sorted(
        REQUIRED_GOVERNING_PRINCIPLE_IDS | REQUIRED_REASONING_LENS_IDS
    ):
        if f"`{identifier}`" not in registry_text:
            errors.append(f"principle registry is missing `{identifier}`")


def validate_reference_structure(errors: list[str]) -> None:
    for path in sorted(SKILLS_DIR.glob("*/references/**/*")):
        if not path.is_file():
            continue
        relative = path.relative_to(ROOT)
        if path.parent.name != "references":
            errors.append(f"nested reference file is not allowed: {relative}")
            continue

        lines = path.read_text(encoding="utf-8").splitlines()
        if SHIPPING_PLACEHOLDER.search("\n".join(lines)):
            errors.append(f"shipping placeholder in {relative}")
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
    cases_by_id: dict[str, dict[str, Any]] = {}
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
            cases_by_id[case_id] = case
            label = f"eval {case_id}"

        controller = case.get("expected_controller")
        if controller not in skill_names:
            errors.append(f"{label} names unknown controller: {controller!r}")

        mode = case.get("expected_mode")
        if mode not in ALLOWED_MODES:
            errors.append(f"{label} has unsupported mode: {mode!r}")
        elif controller in CONTROLLER_MODES and mode not in CONTROLLER_MODES[controller]:
            errors.append(
                f"{label} uses mode {mode!r}, which controller {controller!r} "
                "does not support"
            )

        routes = case.get("expected_routes", [])
        if not isinstance(routes, list):
            errors.append(f"{label} expected_routes must be a list")
        else:
            if len(routes) != len(set(routes)):
                errors.append(f"{label} expected_routes contains duplicates")
            if controller in routes:
                errors.append(f"{label} routes its controller to itself")
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

    missing_guardrails = sorted(REQUIRED_GUARDRAIL_EVAL_IDS - seen_ids)
    if missing_guardrails:
        errors.append(
            "missing required guardrail evals: " + ", ".join(missing_guardrails)
        )

    for case_id, contract in REQUIRED_EVOLUTION_EVAL_CONTRACTS.items():
        case = cases_by_id.get(case_id)
        if case is None:
            errors.append(f"missing required evolution eval: {case_id}")
            continue

        if case.get("expected_controller") != contract["controller"]:
            errors.append(
                f"evolution eval {case_id} must use controller "
                f"{contract['controller']!r}"
            )
        if case.get("expected_mode") != contract["mode"]:
            errors.append(
                f"evolution eval {case_id} must use mode {contract['mode']!r}"
            )
        routes = case.get("expected_routes", [])
        if isinstance(routes, list) and set(routes) != contract["routes"]:
            errors.append(
                f"evolution eval {case_id} has the wrong route contract"
            )
        for field in ("must", "must_not"):
            values = case.get(field, [])
            if not isinstance(values, list):
                continue
            missing_values = sorted(contract[field] - set(values))
            if missing_values:
                errors.append(
                    f"evolution eval {case_id} is missing required {field} "
                    f"items: {', '.join(missing_values)}"
                )

    evolve_modes = {
        case.get("expected_mode")
        for case in cases_by_id.values()
        if case.get("expected_controller") == "star-writing-evolve"
    }
    missing_evolve_modes = sorted({"audit", "plan", "evolve"} - evolve_modes)
    if missing_evolve_modes:
        errors.append(
            "star-writing-evolve lacks direct eval coverage for modes: "
            + ", ".join(missing_evolve_modes)
        )

    return len(cases)


def main() -> int:
    errors: list[str] = []
    validate_manifest(errors)
    skill_names = validate_skills(errors)
    validate_cross_skill_contracts(skill_names, errors)
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
