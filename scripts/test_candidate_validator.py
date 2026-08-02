#!/usr/bin/env python3
"""Exercise the evolution-candidate validator in an isolated Git fixture."""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path


SOURCE_ROOT = Path(__file__).resolve().parents[1]
CANDIDATE_NAME = "EVO-20260802T120000Z-regression-contract.md"
SOURCE_VERSION = json.loads(
    (SOURCE_ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
)["version"]


def run(command: list[str], root: Path, *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=root,
        check=check,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        timeout=30,
    )


def git(root: Path, *args: str) -> str:
    return run(["git", *args], root).stdout.strip()


def candidate_text(
    baseline: str,
    *,
    record_revision: int = 1,
    updated_at: str = "2026-08-02T12:00:00Z",
    activation: str = "none",
    status: str = "triaged",
    decision: str = "investigate",
    scope_layer: str = "unresolved",
    target_owner: str = "unresolved",
    review_after: str = "none",
    implemented_revision: str = "none",
    validated_snapshot: str = "none",
    episode_suffix: str = "",
) -> str:
    return f"""---
schema_version: 1
id: {CANDIDATE_NAME.removesuffix('.md')}
record_revision: {record_revision}
created_at: 2026-08-02T12:00:00Z
updated_at: {updated_at}
source_skill: star-writing-draft
source_version: {SOURCE_VERSION}
baseline_revision: {baseline}
activation: {activation}
status: {status}
decision: {decision}
scope_layer: {scope_layer}
root_cause: instruction-gap
rule_health: not-applicable
target_owner: {target_owner}
review_after: {review_after}
implemented_revision: {implemented_revision}
validated_snapshot: {validated_snapshot}
persistence_authorized: true
visibility: public-safe
privacy_review: passed
---

# Regression-contract candidate

## Episode

An authorized maintenance exercise exposed a reusable validation question.
{episode_suffix}

## Diagnosis and scope

The narrow hypothesis concerns candidate-ledger controls, not paper behavior.

## Candidate behavior

Reject malformed provenance while leaving every active instruction unchanged.

## Evidence and risk

The fixture covers one positive case and nearby failures without claiming use.

## Authorization boundary

Only this isolated fixture is writable; source, adoption, and Git remain out.

## Validation and disposition

Run the suite validator and retain this candidate as inactive test evidence.
"""


def validate(root: Path) -> subprocess.CompletedProcess[str]:
    return run(
        ["python3", "scripts/validate_plugin_suite.py"], root, check=False
    )


def snapshot(root: Path) -> str:
    return run(
        ["python3", "scripts/validate_plugin_suite.py", "--print-source-snapshot"],
        root,
    ).stdout.strip()


def require_success(result: subprocess.CompletedProcess[str], label: str) -> None:
    if result.returncode != 0:
        raise AssertionError(f"{label} unexpectedly failed:\n{result.stdout}")


def require_failure(
    result: subprocess.CompletedProcess[str], label: str, expected: str
) -> None:
    if result.returncode == 0:
        raise AssertionError(f"{label} unexpectedly passed")
    if expected not in result.stdout:
        raise AssertionError(
            f"{label} missed diagnostic {expected!r}:\n{result.stdout}"
        )


def main() -> int:
    with tempfile.TemporaryDirectory(
        prefix="star-writing-candidate-regression-"
    ) as temporary:
        fixture = Path(temporary) / "star-writing-skills"
        shutil.copytree(
            SOURCE_ROOT,
            fixture,
            ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"),
        )
        fixture_candidates = fixture / "evolution" / "candidates"
        for existing in fixture_candidates.glob("*.md"):
            if existing.name != "README.md":
                existing.unlink()
        git(fixture, "init", "--quiet")
        git(fixture, "config", "user.name", "Validator Fixture")
        git(fixture, "config", "user.email", "fixture@example.invalid")
        git(fixture, "add", ".")
        git(fixture, "commit", "--quiet", "-m", "fixture source")
        baseline = git(fixture, "rev-parse", "HEAD")
        fixture_tree = git(fixture, "write-tree")
        unrelated = git(
            fixture, "commit-tree", fixture_tree, "-m", "unrelated fixture source"
        )

        candidate = fixture / "evolution" / "candidates" / CANDIDATE_NAME
        valid_v1 = candidate_text(baseline)
        candidate.write_text(valid_v1, encoding="utf-8")
        require_success(validate(fixture), "valid revision-one candidate")

        candidate.write_text(
            candidate_text(baseline, activation="active"), encoding="utf-8"
        )
        require_failure(validate(fixture), "active candidate", "required activation")

        candidate.write_text(
            candidate_text(
                baseline,
                status="proposed",
                decision="extend",
                scope_layer="shared-policy",
                target_owner=f"evolution/candidates/{CANDIDATE_NAME}",
            ),
            encoding="utf-8",
        )
        require_failure(
            validate(fixture), "self-owning candidate", "non-portable target_owner"
        )

        candidate.write_text(
            candidate_text(
                baseline,
                status="proposed",
                decision="extend",
                scope_layer="focused-skill",
                target_owner="skills/star-writing-draft",
            ),
            encoding="utf-8",
        )
        require_failure(
            validate(fixture), "directory target owner", "non-portable target_owner"
        )

        candidate.write_text(
            candidate_text(
                baseline,
                status="proposed",
                decision="extend",
                scope_layer="project-state",
                target_owner="skills/star-writing-draft/SKILL.md",
            ),
            encoding="utf-8",
        )
        require_failure(
            validate(fixture), "local-to-global scope", "local scope requires"
        )

        private_marker = "Contact: " + "fixture" + "@example.invalid"
        candidate.write_text(
            candidate_text(baseline, episode_suffix=private_marker),
            encoding="utf-8",
        )
        require_failure(validate(fixture), "private candidate", "email address")

        comment_only = valid_v1.replace(
            "An authorized maintenance exercise exposed a reusable validation question.\n",
            "<!-- This comment does not provide candidate evidence. -->\n",
        )
        candidate.write_text(comment_only, encoding="utf-8")
        require_failure(
            validate(fixture), "comment-only section", "empty or trivial"
        )

        inline_headings = valid_v1
        for heading in (
            "## Episode",
            "## Diagnosis and scope",
            "## Candidate behavior",
            "## Evidence and risk",
            "## Authorization boundary",
            "## Validation and disposition",
        ):
            inline_headings = inline_headings.replace(
                f"\n{heading}\n", f"\nInline marker {heading}\n"
            )
        candidate.write_text(inline_headings, encoding="utf-8")
        require_failure(
            validate(fixture), "inline heading markers", "missing heading"
        )

        candidate.write_text(valid_v1, encoding="utf-8")
        private_entry = (
            fixture
            / "evolution"
            / "candidates"
            / ("alice" + "@example.invalid.txt")
        )
        private_entry.write_text("invalid ledger entry", encoding="utf-8")
        redacted_result = validate(fixture)
        require_failure(
            redacted_result,
            "private malformed filename",
            "unexpected candidate-ledger entry",
        )
        if (
            "alice" in redacted_result.stdout
            or "example.invalid" in redacted_result.stdout
        ):
            raise AssertionError("malformed-entry diagnostic leaked its filename")
        private_entry.unlink()

        candidate.write_text(
            candidate_text(
                baseline,
                status="validated",
                decision="extend",
                scope_layer="focused-skill",
                target_owner="skills/star-writing-draft/SKILL.md",
            ),
            encoding="utf-8",
        )
        require_failure(
            validate(fixture), "receipt-free validation", "snapshot receipt"
        )

        candidate.write_text(
            candidate_text(
                baseline,
                status="validated",
                decision="extend",
                scope_layer="focused-skill",
                target_owner="skills/star-writing-draft/SKILL.md",
                validated_snapshot="sha256:" + ("0" * 64),
            ),
            encoding="utf-8",
        )
        require_failure(
            validate(fixture), "invented SHA receipt", "does not match current source"
        )

        candidate.write_text(
            candidate_text(
                baseline,
                status="implemented",
                decision="extend",
                scope_layer="focused-skill",
                target_owner="skills/star-writing-draft/SKILL.md",
            ),
            encoding="utf-8",
        )
        require_failure(
            validate(fixture),
            "empty implementation state",
            "uncommitted implementation leaves target_owner unchanged",
        )

        owner = fixture / "skills" / "star-writing-draft" / "SKILL.md"
        owner_before = owner.read_text(encoding="utf-8")
        owner.write_text(
            owner_before + "\n<!-- isolated candidate-regression change -->\n",
            encoding="utf-8",
        )
        candidate.write_text(
            candidate_text(
                baseline,
                status="implemented",
                decision="extend",
                scope_layer="focused-skill",
                target_owner="skills/star-writing-draft/SKILL.md",
            ),
            encoding="utf-8",
        )
        require_success(validate(fixture), "valid uncommitted implementation")
        current_snapshot = snapshot(fixture)
        candidate.write_text(
            candidate_text(
                baseline,
                status="validated",
                decision="extend",
                scope_layer="focused-skill",
                target_owner="skills/star-writing-draft/SKILL.md",
                validated_snapshot=current_snapshot,
            ),
            encoding="utf-8",
        )
        require_success(validate(fixture), "valid working-source snapshot receipt")
        owner.write_text(owner_before, encoding="utf-8")

        candidate.write_text(
            candidate_text(unrelated), encoding="utf-8"
        )
        require_failure(
            validate(fixture),
            "unrelated baseline",
            "outside current source history",
        )

        candidate.write_text(
            candidate_text(
                baseline,
                status="validated",
                decision="extend",
                scope_layer="focused-skill",
                target_owner="skills/star-writing-draft/SKILL.md",
                validated_snapshot="commit:" + ("0" * 40),
            ),
            encoding="utf-8",
        )
        require_failure(
            validate(fixture), "nonexistent validation commit", "not a Git commit"
        )

        candidate.write_text(
            candidate_text(
                baseline,
                status="committed",
                decision="extend",
                scope_layer="focused-skill",
                target_owner="skills/star-writing-draft/SKILL.md",
                implemented_revision=baseline,
                validated_snapshot=f"commit:{baseline}",
            ),
            encoding="utf-8",
        )
        require_failure(
            validate(fixture),
            "baseline-as-implementation receipt",
            "implementation does not descend from baseline",
        )

        readme = fixture / "README.md"
        readme.write_text(
            readme.read_text(encoding="utf-8")
            + "\n<!-- unrelated fixture commit -->\n",
            encoding="utf-8",
        )
        git(fixture, "add", "README.md")
        git(fixture, "commit", "--quiet", "-m", "unrelated descendant")
        unrelated_descendant = git(fixture, "rev-parse", "HEAD")
        candidate.write_text(
            candidate_text(
                baseline,
                status="committed",
                decision="extend",
                scope_layer="focused-skill",
                target_owner="skills/star-writing-draft/SKILL.md",
                implemented_revision=unrelated_descendant,
                validated_snapshot=f"commit:{unrelated_descendant}",
            ),
            encoding="utf-8",
        )
        require_failure(
            validate(fixture),
            "unrelated implementation commit",
            "leaves target_owner unchanged",
        )

        owner.write_text(
            owner_before + "\n<!-- implementation fixture A -->\n",
            encoding="utf-8",
        )
        git(fixture, "add", "skills/star-writing-draft/SKILL.md")
        git(fixture, "commit", "--quiet", "-m", "implementation fixture A")
        implementation_a = git(fixture, "rev-parse", "HEAD")
        owner.write_text(
            owner.read_text(encoding="utf-8")
            + "\n<!-- implementation fixture B -->\n",
            encoding="utf-8",
        )
        git(fixture, "add", "skills/star-writing-draft/SKILL.md")
        git(fixture, "commit", "--quiet", "-m", "implementation fixture B")
        implementation_b = git(fixture, "rev-parse", "HEAD")
        candidate.write_text(
            candidate_text(
                baseline,
                status="validated",
                decision="extend",
                scope_layer="focused-skill",
                target_owner="skills/star-writing-draft/SKILL.md",
                implemented_revision=implementation_b,
                validated_snapshot=f"commit:{implementation_a}",
            ),
            encoding="utf-8",
        )
        require_failure(
            validate(fixture),
            "validation predates implementation",
            "does not descend from implemented_revision",
        )

        candidate.write_text(valid_v1, encoding="utf-8")
        git(fixture, "add", f"evolution/candidates/{CANDIDATE_NAME}")
        git(fixture, "commit", "--quiet", "-m", "candidate revision one")

        candidate.write_text(
            candidate_text(
                baseline,
                record_revision=2,
                updated_at="2026-08-02T12:00:01Z",
                status="proposed",
                decision="extend",
                scope_layer="focused-skill",
                target_owner="skills/star-writing-draft/SKILL.md",
            ),
            encoding="utf-8",
        )
        require_success(validate(fixture), "valid monotonic candidate update")

        candidate.write_text(
            candidate_text(
                baseline,
                record_revision=2,
                updated_at="2026-08-02T12:00:01Z",
                status="observed",
            ),
            encoding="utf-8",
        )
        require_failure(
            validate(fixture), "backward lifecycle update", "lifecycle transition"
        )

        candidate.write_text(
            candidate_text(baseline, record_revision=2), encoding="utf-8"
        )
        require_failure(
            validate(fixture), "stale update timestamp", "advance updated_at"
        )

        candidate.write_text(
            candidate_text(
                baseline,
                record_revision=2,
                updated_at="2026-08-02T12:00:01Z",
                status="rework",
                review_after="2026-08-03",
            ),
            encoding="utf-8",
        )
        require_success(validate(fixture), "valid rework transition")
        git(fixture, "add", f"evolution/candidates/{CANDIDATE_NAME}")
        git(fixture, "commit", "--quiet", "-m", "candidate enters rework")

        candidate.write_text(
            candidate_text(
                baseline,
                record_revision=3,
                updated_at="2026-08-02T12:00:02Z",
                status="proposed",
                decision="extend",
                scope_layer="focused-skill",
                target_owner="skills/star-writing-draft/SKILL.md",
            ),
            encoding="utf-8",
        )
        require_failure(
            validate(fixture), "rework skips triage", "lifecycle transition"
        )

    print("Evolution-candidate validator regression passed: 5 positive and 19 negative checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
