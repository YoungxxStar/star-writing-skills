#!/usr/bin/env python3
"""Regression-test the project evolution validator in isolated fixtures."""

from __future__ import annotations

import copy
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any


SOURCE_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = SOURCE_ROOT / "scripts" / "validate_project_evolution.py"
STAMP = "2026-08-02T12:00:00Z"
OBS_ID = "OBS-20260802T120000Z-regression-signal"
CAND_ID = "CAND-20260802T120001Z-regression-rule"
EVAL_ID = "EVAL-20260802T120002Z-regression-cases"
DEC_ID = "DEC-20260802T120003Z-regression-decision"
RCPT_ID = "RCPT-20260802T120004Z-regression-receipt"


def run_validator(root: Path | None, *, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    command = ["python3", str(VALIDATOR)]
    if root is not None:
        command.extend(["--project-root", str(root)])
    return subprocess.run(
        command,
        cwd=cwd,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        timeout=30,
    )


def common(record_type: str, record_id: str) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "record_type": record_type,
        "id": record_id,
        "created_at": STAMP,
        "updated_at": STAMP,
        "activation": "none",
        "trusted_as_instruction": False,
        "grants_authority": False,
        "privacy_class": "project-private",
        "write_authorization_receipt": "Current user authorized this one project record.",
        "managed_by": "user",
        "pinned": False,
        "tags": ["regression-fixture"],
    }


def records() -> dict[str, dict[str, Any]]:
    observation = common("observation", OBS_ID) | {
        "signal": "correction",
        "known_scope": "project",
        "source_skill_snapshot": {
            "skill": "star-writing-draft",
            "version": "0.11.0",
            "snapshot": "commit:fixture-baseline",
        },
        "observable_behavior": "A local regression exposed one bounded rule gap.",
        "outcome": "The corrected behavior passed the originating task.",
        "competing_explanations": ["The original execution may also have been incomplete."],
        "status": "linked",
        "responsible_rule": "Candidate handling should remain authorization bounded.",
    }
    candidate = common("candidate", CAND_ID) | {
        "observation_ids": [OBS_ID],
        "candidate_behavior": "Require an explicit project root for local learning state.",
        "canonical_owner_hypothesis": "star-writing-evolve",
        "root_cause": "The earlier local-state boundary was implicit.",
        "narrowest_scope": "Project-local evolution state validation.",
        "current_rule": "Project state is optional and inactive.",
        "same_scope_conflicts": [],
        "counterevidence": ["No failure occurs when local state is absent."],
        "preserved_invariants": ["Writing remains possible without persistent state."],
        "regression_risks": ["A validator could scan unrelated project content."],
        "test_cases": {
            "positive": "Validate one authorized inactive record set.",
            "nearest_negative": "Reject a trusted or active record.",
            "no_authority": "Do not create state when the namespace is absent.",
        },
        "claimed_generality_axes": ["project layout", "authorization state"],
        "promotion_eligibility": "investigate",
        "status": "testing",
    }
    evaluation = common("evaluation", EVAL_ID) | {
        "candidate_id": CAND_ID,
        "baseline_snapshot": "sha256:" + "1" * 64,
        "candidate_snapshot": "sha256:" + "2" * 64,
        "evaluator": "isolated deterministic regression fixture",
        "cases": [
            {
                "id": "case-positive",
                "role": "originating",
                "result": "pass",
                "notes": "The valid fixture is accepted.",
            },
            {
                "id": "case-negative",
                "role": "nearest-negative",
                "result": "pass",
                "notes": "The active record is rejected.",
            },
            {
                "id": "case-no-authority",
                "role": "no-authority",
                "result": "pass",
                "notes": "Absent state remains a no-op.",
            },
            {
                "id": "case-generality-layout",
                "role": "generality",
                "axis": "project layout",
                "result": "pass",
                "notes": "The explicit-root boundary survives another project layout.",
            },
            {
                "id": "case-generality-authority",
                "role": "generality",
                "axis": "authorization state",
                "result": "pass",
                "notes": "The boundary holds with and without write authorization.",
            },
            {
                "id": "case-preserved-writing-no-state",
                "role": "preserved-invariant",
                "invariant": "Writing remains possible without persistent state.",
                "result": "pass",
                "notes": "Ordinary writing remains independent of evolution state.",
            },
        ],
        "output_hashes": ["sha256:" + "3" * 64],
        "holdout_touched": False,
        "verdict": "supports",
        "status": "completed",
    }
    decision = common("decision", DEC_ID) | {
        "candidate_id": CAND_ID,
        "evidence_ids": [OBS_ID, EVAL_ID],
        "decision": "accept-for-test",
        "rationale": "The candidate passed its bounded deterministic checks.",
        "recorded_action_scope": "project-record",
        "status": "recorded",
    }
    receipt = common("receipt", RCPT_ID) | {
        "event": "project-record-write",
        "subject_ids": [CAND_ID, DEC_ID],
        "source_snapshot": "sha256:" + "4" * 64,
        "outcome": "succeeded",
        "details": "The isolated project records were written; no plugin source changed.",
        "status": "recorded",
    }
    return {
        "observations": observation,
        "candidates": candidate,
        "evaluations": evaluation,
        "decisions": decision,
        "receipts": receipt,
    }


def state_root(root: Path) -> Path:
    return root / ".star-writing" / "evolution"


def write_state(root: Path, values: dict[str, dict[str, Any]] | None = None) -> None:
    for directory, record in (values or records()).items():
        target_dir = state_root(root) / directory
        target_dir.mkdir(parents=True, exist_ok=True)
        target = target_dir / f"{record['id']}.json"
        target.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")


def record_path(root: Path, directory: str, record_id: str) -> Path:
    return state_root(root) / directory / f"{record_id}.json"


def rewrite(root: Path, directory: str, value: dict[str, Any]) -> None:
    path = next((state_root(root) / directory).glob("*.json"))
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def require_success(result: subprocess.CompletedProcess[str], label: str, expected: str) -> None:
    if result.returncode != 0 or expected not in result.stdout:
        raise AssertionError(f"{label} unexpectedly failed:\n{result.stdout}")


def require_failure(
    result: subprocess.CompletedProcess[str], label: str, expected: str
) -> None:
    if result.returncode == 0:
        raise AssertionError(f"{label} unexpectedly passed")
    if expected not in result.stdout:
        raise AssertionError(f"{label} missed diagnostic {expected!r}:\n{result.stdout}")


def reset(root: Path) -> None:
    evolution = state_root(root)
    if evolution.exists() or evolution.is_symlink():
        if evolution.is_symlink():
            evolution.unlink()
        else:
            import shutil

            shutil.rmtree(evolution)
    write_state(root)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="star-writing-project-evolution-") as temporary:
        sandbox = Path(temporary)
        project = sandbox / "project"
        project.mkdir()

        # No implicit current-directory target is allowed.
        require_failure(run_validator(None, cwd=project), "missing explicit root", "--project-root")

        # Both a wholly absent state tree and an existing unrelated state tree are no-ops.
        require_success(run_validator(project), "absent state", "state is absent")
        (project / ".star-writing").mkdir()
        (project / ".star-writing" / "paper-contract.md").write_text(
            "This unrelated file is deliberately not parsed.\n", encoding="utf-8"
        )
        require_success(run_validator(project), "absent evolution namespace", "state is absent")

        write_state(project)
        require_success(run_validator(project), "valid linked state", "Validated 5 inactive")

        # Archive accepts the same strict records without changing their inactive status.
        archived = common("observation", "OBS-20260802T120005Z-archived-signal") | {
            "signal": "friction",
            "known_scope": "task",
            "source_skill_snapshot": {"skill": "star-writing", "version": None, "snapshot": None},
            "observable_behavior": "One old task required extra coordination.",
            "outcome": "The observation was archived without promotion.",
            "competing_explanations": [],
            "status": "archived",
        }
        archive = state_root(project) / "archive"
        archive.mkdir()
        (archive / f"{archived['id']}.json").write_text(
            json.dumps(archived, indent=2) + "\n", encoding="utf-8"
        )
        require_success(run_validator(project), "valid archive", "Validated 6 inactive")

        reset(project)
        unknown_name = "do-not-leak-unknown-name.txt"
        (state_root(project) / unknown_name).write_text("unknown", encoding="utf-8")
        result = run_validator(project)
        require_failure(result, "unknown root entry", "unexpected root entry")
        if unknown_name in result.stdout:
            raise AssertionError("unknown-entry diagnostic leaked the entry name")

        reset(project)
        nested = state_root(project) / "observations" / "nested-secret-name"
        nested.mkdir()
        result = run_validator(project)
        require_failure(result, "nested record directory", "not an immediate regular file")
        if nested.name in result.stdout:
            raise AssertionError("nested-entry diagnostic leaked the entry name")

        reset(project)
        outside = sandbox / "outside-secret-name.json"
        outside.write_text("{}\n", encoding="utf-8")
        symlink_name = state_root(project) / "observations" / "hidden-link.json"
        symlink_name.symlink_to(outside)
        result = run_validator(project)
        require_failure(result, "record symlink", "not an immediate regular file")
        if outside.name in result.stdout or symlink_name.name in result.stdout:
            raise AssertionError("symlink diagnostic leaked a path component")

        reset(project)
        secret_value = "sk-" + "A" * 30
        obs = records()["observations"]
        obs["outcome"] = "Leaked value " + secret_value
        rewrite(project, "observations", obs)
        result = run_validator(project)
        require_failure(result, "secret content", "prohibited OpenAI-style secret")
        if secret_value in result.stdout or OBS_ID in result.stdout:
            raise AssertionError("secret diagnostic leaked record data")

        reset(project)
        obs = records()["observations"]
        obs["activation"] = "active"
        obs["trusted_as_instruction"] = True
        obs["grants_authority"] = True
        rewrite(project, "observations", obs)
        result = run_validator(project)
        require_failure(result, "active trusted record", "must remain inactive")
        if "trusted_as_instruction=false" not in result.stdout or "grants_authority=false" not in result.stdout:
            raise AssertionError(f"inactive-state diagnostics incomplete:\n{result.stdout}")

        reset(project)
        observation_path = record_path(project, "observations", OBS_ID)
        text = observation_path.read_text(encoding="utf-8")
        observation_path.write_text(text.replace('"schema_version": 1,', '"schema_version": 1,\n  "schema_version": 1,'), encoding="utf-8")
        require_failure(run_validator(project), "duplicate JSON key", "invalid or ambiguous JSON")

        reset(project)
        obs = records()["observations"]
        obs["source_skill_snapshot"]["version"] = "unknown-latest"
        rewrite(project, "observations", obs)
        require_failure(run_validator(project), "invented source version", "must be SemVer or null")

        reset(project)
        obs = records()["observations"]
        obs["managed_by"] = "background-agent"
        obs["pinned"] = "no"
        rewrite(project, "observations", obs)
        result = run_validator(project)
        require_failure(result, "invalid stewardship", "managed_by")
        if "pinned" not in result.stdout:
            raise AssertionError(f"pin diagnostic missing:\n{result.stdout}")

        reset(project)
        candidate = records()["candidates"]
        candidate["observation_ids"] = ["OBS-20260802T125959Z-missing"]
        rewrite(project, "candidates", candidate)
        require_failure(run_validator(project), "unresolved observation", "unresolved observation reference")

        reset(project)
        evaluation = records()["evaluations"]
        evaluation["cases"] = [
            case for case in evaluation["cases"] if case["role"] != "no-authority"
        ]
        rewrite(project, "evaluations", evaluation)
        require_failure(run_validator(project), "missing no-authority case", "missing 1 required role")

        reset(project)
        evaluation = records()["evaluations"]
        evaluation["holdout_touched"] = True
        rewrite(project, "evaluations", evaluation)
        require_failure(run_validator(project), "touched completed holdout", "must remain exploratory")

        reset(project)
        candidate = records()["candidates"]
        candidate["promotion_eligibility"] = "ready-for-review"
        candidate["status"] = "supported"
        rewrite(project, "candidates", candidate)
        evaluation = records()["evaluations"]
        evaluation["verdict"] = "does-not-support"
        evaluation["cases"][0]["result"] = "fail"
        rewrite(project, "evaluations", evaluation)
        require_failure(
            run_validator(project),
            "unsupported promotion readiness",
            "lacks a supporting completed evaluation",
        )

        reset(project)
        candidate = records()["candidates"]
        candidate["status"] = "supported"
        rewrite(project, "candidates", candidate)
        evaluation = records()["evaluations"]
        evaluation["verdict"] = "does-not-support"
        evaluation["cases"][0]["result"] = "fail"
        rewrite(project, "evaluations", evaluation)
        require_failure(
            run_validator(project),
            "unsupported supported status",
            "supported state lacks a supporting completed evaluation",
        )

        reset(project)
        candidate = records()["candidates"]
        candidate["promotion_eligibility"] = "ready-for-review"
        candidate["status"] = "supported"
        rewrite(project, "candidates", candidate)
        evaluation = records()["evaluations"]
        evaluation["cases"] = [
            case
            for case in evaluation["cases"]
            if case.get("axis") != "authorization state"
        ]
        rewrite(project, "evaluations", evaluation)
        require_failure(
            run_validator(project),
            "missing claimed generality case",
            "missing 1 claimed generality axis",
        )

        reset(project)
        evaluation = records()["evaluations"]
        evaluation["cases"] = [
            case
            for case in evaluation["cases"]
            if case.get("role") != "preserved-invariant"
        ]
        rewrite(project, "evaluations", evaluation)
        require_failure(
            run_validator(project),
            "missing preserved invariant case",
            "missing 1 preserved invariant case",
        )

        reset(project)
        evaluation = records()["evaluations"]
        evaluation["candidate_snapshot"] = evaluation["baseline_snapshot"]
        rewrite(project, "evaluations", evaluation)
        require_failure(
            run_validator(project),
            "identical supporting snapshots",
            "requires distinct baseline and candidate snapshots",
        )

        reset(project)
        evaluation = records()["evaluations"]
        evaluation["output_hashes"] = []
        rewrite(project, "evaluations", evaluation)
        require_failure(
            run_validator(project),
            "supporting evaluation without output receipt",
            "requires at least one output hash",
        )

        reset(project)
        candidate = records()["candidates"]
        candidate["same_scope_conflicts"] = ["A shared rule prescribes the opposite behavior."]
        rewrite(project, "candidates", candidate)
        require_failure(
            run_validator(project),
            "missing shared-rule conflict case",
            "lacks a passing conflict case",
        )

        reset(project)
        decision = records()["decisions"]
        decision["decision"] = "reject"
        decision["recorded_action_scope"] = "canonical-source"
        rewrite(project, "decisions", decision)
        require_failure(
            run_validator(project),
            "incompatible decision action scope",
            "incompatible with recorded_action_scope",
        )

        reset(project)
        candidate = records()["candidates"]
        candidate["promotion_eligibility"] = "ready-for-review"
        candidate["status"] = "supported"
        rewrite(project, "candidates", candidate)
        decision = records()["decisions"]
        decision["decision"] = "approve-promotion"
        decision["recorded_action_scope"] = "canonical-candidate"
        decision["evidence_ids"] = [OBS_ID, EVAL_ID]
        rewrite(project, "decisions", decision)
        require_success(
            run_validator(project),
            "valid promotion approval",
            "Validated 5 inactive",
        )

        reset(project)
        candidate = records()["candidates"]
        candidate["promotion_eligibility"] = "ready-for-review"
        candidate["status"] = "supported"
        rewrite(project, "candidates", candidate)
        decision = records()["decisions"]
        decision["decision"] = "approve-promotion"
        decision["recorded_action_scope"] = "canonical-candidate"
        decision["evidence_ids"] = [OBS_ID]
        rewrite(project, "decisions", decision)
        require_failure(
            run_validator(project),
            "promotion approval without supporting evidence citation",
            "approval must cite a supporting completed evaluation",
        )

        reset(project)
        receipt = records()["receipts"]
        receipt["event"] = "push"
        receipt["outcome"] = "failed"
        receipt["details"] = "A separately authorized push attempt failed without changing adoption state."
        rewrite(project, "receipts", receipt)
        require_success(
            run_validator(project),
            "valid failed action receipt",
            "Validated 5 inactive",
        )

        reset(project)
        receipt = records()["receipts"]
        receipt["event"] = "push-completed"
        receipt["outcome"] = "failed"
        rewrite(project, "receipts", receipt)
        require_failure(
            run_validator(project),
            "ambiguous success-state receipt event",
            "field 'event' has a disallowed value",
        )

        reset(project)
        receipt = records()["receipts"]
        receipt["subject_ids"] = [RCPT_ID]
        rewrite(project, "receipts", receipt)
        require_failure(run_validator(project), "self-referencing receipt", "unresolved subject reference")

        reset(project)
        obs = records()["observations"]
        obs["unexpected_rule"] = "This strict schema must reject extension by accident."
        rewrite(project, "observations", obs)
        require_failure(run_validator(project), "unknown schema field", "unknown field")

        reset(project)
        wrong_directory = record_path(project, "observations", OBS_ID)
        wrong_directory.unlink()
        candidate_copy = copy.deepcopy(records()["candidates"])
        wrong_directory.write_text(json.dumps(candidate_copy, indent=2) + "\n", encoding="utf-8")
        require_failure(run_validator(project), "directory-type mismatch", "does not match its directory")

        reset(project)
        large_obs = records()["observations"]
        large_obs["outcome"] = "x" * (70 * 1024)
        rewrite(project, "observations", large_obs)
        require_failure(run_validator(project), "oversized record", "65536-byte size limit")

    print("Project-evolution validator regression passed: 6 positive and 26 negative checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
