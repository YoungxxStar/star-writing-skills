#!/usr/bin/env python3
"""Validate inactive project-local STAR Writing evolution records.

The validator deliberately has no current-working-directory default. Callers
must bind one project explicitly::

    python3 scripts/validate_project_evolution.py --project-root /path/to/project

Only ``.star-writing/evolution`` below that root is inspected. Its absence is a
valid no-op. The validator never reads manuscript files, plugin source, Git
state, or sibling project-state files. Project evolution records are treated as
untrusted evidence: every valid record must be inactive and must explicitly
deny instruction and authority status.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import stat
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RECORD_DIRECTORIES = {
    "observations": "observation",
    "candidates": "candidate",
    "evaluations": "evaluation",
    "decisions": "decision",
    "receipts": "receipt",
}
OPTIONAL_DIRECTORIES = {"archive"}
ALLOWED_DIRECTORIES = set(RECORD_DIRECTORIES) | OPTIONAL_DIRECTORIES
MAX_RECORD_BYTES = 64 * 1024

COMMON_REQUIRED = {
    "schema_version",
    "record_type",
    "id",
    "created_at",
    "updated_at",
    "activation",
    "trusted_as_instruction",
    "grants_authority",
    "privacy_class",
    "write_authorization_receipt",
    "managed_by",
    "pinned",
}
COMMON_OPTIONAL = {"tags"}

TYPE_FIELDS: dict[str, tuple[set[str], set[str]]] = {
    "observation": (
        {
            "signal",
            "known_scope",
            "source_skill_snapshot",
            "observable_behavior",
            "outcome",
            "competing_explanations",
            "status",
        },
        {"responsible_rule"},
    ),
    "candidate": (
        {
            "observation_ids",
            "candidate_behavior",
            "canonical_owner_hypothesis",
            "root_cause",
            "narrowest_scope",
            "current_rule",
            "same_scope_conflicts",
            "counterevidence",
            "preserved_invariants",
            "regression_risks",
            "test_cases",
            "claimed_generality_axes",
            "promotion_eligibility",
            "status",
        },
        set(),
    ),
    "evaluation": (
        {
            "candidate_id",
            "baseline_snapshot",
            "candidate_snapshot",
            "evaluator",
            "cases",
            "output_hashes",
            "holdout_touched",
            "verdict",
            "status",
        },
        set(),
    ),
    "decision": (
        {
            "candidate_id",
            "evidence_ids",
            "decision",
            "rationale",
            "recorded_action_scope",
            "status",
        },
        {"supersedes_decision_id"},
    ),
    "receipt": (
        {
            "event",
            "subject_ids",
            "source_snapshot",
            "outcome",
            "details",
            "status",
        },
        set(),
    ),
}

TYPE_PREFIX = {
    "observation": "OBS",
    "candidate": "CAND",
    "evaluation": "EVAL",
    "decision": "DEC",
    "receipt": "RCPT",
}
ID_RE = re.compile(
    r"^(OBS|CAND|EVAL|DEC|RCPT)-\d{8}T\d{6}Z-[a-z0-9]+(?:-[a-z0-9]+)*$"
)
TAG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
SEMVER_RE = re.compile(
    r"^(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)

ENUMS = {
    "privacy_class": {"public-safe", "project-private", "restricted"},
    "managed_by": {"user", "agent"},
    "signal": {
        "correction",
        "accepted-result",
        "failure",
        "friction",
        "self-discovery",
    },
    "known_scope": {
        "task",
        "author",
        "project",
        "publication",
        "potentially-reusable",
    },
    "observation_status": {"observed", "linked", "archived"},
    "promotion_eligibility": {"no", "investigate", "ready-for-review"},
    "candidate_status": {
        "triaged",
        "testing",
        "supported",
        "rejected",
        "deferred",
        "rework",
        "archived",
    },
    "evaluation_role": {
        "originating",
        "nearest-negative",
        "no-authority",
        "generality",
        "conflict",
        "preserved-invariant",
    },
    "evaluation_result": {"pass", "fail", "inconclusive"},
    "evaluation_verdict": {"supports", "does-not-support", "inconclusive"},
    "evaluation_status": {"exploratory", "completed", "invalidated"},
    "decision": {
        "accept-for-test",
        "localize",
        "reject",
        "defer",
        "revise",
        "approve-promotion",
    },
    "recorded_action_scope": {
        "none",
        "project-record",
        "canonical-candidate",
        "canonical-source",
    },
    "decision_status": {"recorded", "superseded"},
    "receipt_event": {
        "project-record-write",
        "canonical-candidate-write",
        "source-implementation",
        "source-validation",
        "commit-create",
        "push",
        "release-publish",
        "marketplace-stage",
        "installation-generate",
        "new-session-load",
    },
    "receipt_outcome": {"succeeded", "failed", "partial"},
    "receipt_status": {"recorded", "superseded"},
}

DECISION_ACTION_SCOPES = {
    "accept-for-test": {"none", "project-record"},
    "localize": {"none", "project-record"},
    "reject": {"none", "project-record"},
    "defer": {"none", "project-record"},
    "revise": {"none", "project-record"},
    "approve-promotion": {"canonical-candidate", "canonical-source"},
}

# Diagnostics name only the pattern class and record ordinal. They never echo a
# matched value, record ID, filename, or project path.
PROHIBITED_TEXT = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "OpenAI-style secret": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "GitHub-style secret": re.compile(r"\bgh[oprsu]_[A-Za-z0-9]{20,}\b"),
    "AWS access key": re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    "bearer credential": re.compile(r"\bBearer\s+[A-Za-z0-9._~+/-]{16,}={0,2}\b", re.I),
    "credential assignment": re.compile(
        r"\b(?:api[_-]?key|access[_-]?token|auth[_-]?token|password|passwd|secret)"
        r"\s*[:=]\s*[\"']?[^\s\"']{8,}",
        re.I,
    ),
    "credential-bearing URL": re.compile(r"\b[a-z][a-z0-9+.-]*://[^\s/@:]+:[^\s/@]+@", re.I),
    "email address": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    "machine-local absolute path": re.compile(
        r"(?:^|[\s\"'])(?:/(?:Users|home|users|scratch|cephfs|rds)/|[A-Za-z]:\\)"
    ),
}


class DuplicateKeyError(ValueError):
    """Raised when a JSON object repeats a key."""


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError("duplicate object key")
        result[key] = value
    return result


def reject_nonfinite(value: str) -> None:
    raise ValueError(f"non-finite JSON number: {value}")


def nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def string_list(
    value: Any,
    label: str,
    field: str,
    errors: list[str],
    *,
    nonempty: bool = False,
) -> list[str]:
    if not isinstance(value, list) or (nonempty and not value):
        qualifier = "nonempty " if nonempty else ""
        errors.append(f"{label} field {field!r} must be a {qualifier}string array")
        return []
    if any(not nonempty_string(item) for item in value):
        errors.append(f"{label} field {field!r} contains a non-string or empty item")
        return []
    return value


def enum_value(
    record: dict[str, Any], field: str, allowed: set[str], label: str, errors: list[str]
) -> str | None:
    value = record.get(field)
    if value not in allowed:
        errors.append(f"{label} field {field!r} has a disallowed value")
        return None
    return value


def parse_timestamp(value: Any, label: str, field: str, errors: list[str]) -> datetime | None:
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", value):
        errors.append(f"{label} field {field!r} must be a UTC second timestamp ending in Z")
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        errors.append(f"{label} field {field!r} is not a valid UTC timestamp")
        return None


def safe_record_text(path: Path, label: str, errors: list[str]) -> str | None:
    """Read one already-allowlisted file without following a final symlink."""

    try:
        flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
        descriptor = os.open(path, flags)
    except OSError:
        errors.append(f"{label} could not be opened as a regular local record")
        return None
    try:
        info = os.fstat(descriptor)
        if not stat.S_ISREG(info.st_mode):
            errors.append(f"{label} is not a regular file")
            return None
        if info.st_size > MAX_RECORD_BYTES:
            errors.append(f"{label} exceeds the {MAX_RECORD_BYTES}-byte size limit")
            return None
        raw = os.read(descriptor, MAX_RECORD_BYTES + 1)
        if len(raw) > MAX_RECORD_BYTES:
            errors.append(f"{label} exceeds the {MAX_RECORD_BYTES}-byte size limit")
            return None
        try:
            return raw.decode("utf-8")
        except UnicodeDecodeError:
            errors.append(f"{label} is not UTF-8 text")
            return None
    finally:
        os.close(descriptor)


def discover_records(project_root: Path, errors: list[str]) -> tuple[Path | None, list[tuple[str, Path]]]:
    """Return allowlisted immediate records without scanning anything else."""

    state_root = project_root / ".star-writing"
    evolution_root = state_root / "evolution"

    for label, path in (("project state", state_root), ("evolution state", evolution_root)):
        try:
            info = path.lstat()
        except FileNotFoundError:
            return None, []
        except OSError:
            errors.append(f"{label} could not be inspected")
            return None, []
        if stat.S_ISLNK(info.st_mode):
            errors.append(f"{label} must not be a symbolic link")
            return None, []
        if not stat.S_ISDIR(info.st_mode):
            errors.append(f"{label} must be a directory")
            return None, []

    try:
        resolved_root = evolution_root.resolve(strict=True)
        if not resolved_root.is_relative_to(project_root.resolve(strict=True)):
            errors.append("evolution state escapes the explicit project root")
            return None, []
    except (OSError, RuntimeError):
        errors.append("evolution state could not be resolved safely")
        return None, []

    records: list[tuple[str, Path]] = []
    try:
        root_entries = sorted(os.scandir(evolution_root), key=lambda entry: entry.name)
    except OSError:
        errors.append("evolution state entries could not be inspected")
        return evolution_root, []

    for entry_index, entry in enumerate(root_entries, start=1):
        if entry.name not in ALLOWED_DIRECTORIES:
            errors.append(f"evolution state contains unexpected root entry #{entry_index}")
            continue
        try:
            if entry.is_symlink() or not entry.is_dir(follow_symlinks=False):
                errors.append(f"evolution directory entry #{entry_index} is not a local directory")
                continue
        except OSError:
            errors.append(f"evolution directory entry #{entry_index} could not be inspected")
            continue
        directory = Path(entry.path)
        try:
            children = sorted(os.scandir(directory), key=lambda child: child.name)
        except OSError:
            errors.append(f"evolution directory entry #{entry_index} could not be read")
            continue
        for child_index, child in enumerate(children, start=1):
            record_label = f"{entry.name} record #{child_index}"
            try:
                if child.is_symlink() or not child.is_file(follow_symlinks=False):
                    errors.append(f"{record_label} is not an immediate regular file")
                    continue
            except OSError:
                errors.append(f"{record_label} could not be inspected")
                continue
            if Path(child.name).suffix != ".json":
                errors.append(f"{record_label} is not a JSON record")
                continue
            candidate_path = Path(child.path)
            try:
                if not candidate_path.resolve(strict=True).is_relative_to(resolved_root):
                    errors.append(f"{record_label} escapes the evolution namespace")
                    continue
            except (OSError, RuntimeError):
                errors.append(f"{record_label} could not be resolved safely")
                continue
            records.append((entry.name, candidate_path))
    return evolution_root, records


def load_record(path: Path, label: str, errors: list[str]) -> dict[str, Any] | None:
    text = safe_record_text(path, label, errors)
    if text is None:
        return None
    for pattern_name, pattern in PROHIBITED_TEXT.items():
        if pattern.search(text):
            errors.append(f"{label} contains prohibited {pattern_name}")
    try:
        value = json.loads(
            text,
            object_pairs_hook=reject_duplicate_keys,
            parse_constant=reject_nonfinite,
        )
    except json.JSONDecodeError as exc:
        errors.append(f"{label} has invalid JSON syntax at line {exc.lineno}, column {exc.colno}")
        return None
    except (DuplicateKeyError, ValueError, RecursionError):
        errors.append(f"{label} has invalid or ambiguous JSON structure")
        return None
    if not isinstance(value, dict):
        errors.append(f"{label} must contain one JSON object")
        return None
    return value


def validate_common(
    record: dict[str, Any], path: Path, directory: str, label: str, errors: list[str]
) -> str | None:
    record_type = record.get("record_type")
    if record_type not in TYPE_FIELDS:
        errors.append(f"{label} field 'record_type' has a disallowed value")
        return None

    required, optional = TYPE_FIELDS[record_type]
    allowed_fields = COMMON_REQUIRED | COMMON_OPTIONAL | required | optional
    missing = (COMMON_REQUIRED | required) - set(record)
    extra = set(record) - allowed_fields
    if missing:
        errors.append(f"{label} is missing {len(missing)} required field(s)")
    if extra:
        errors.append(f"{label} contains {len(extra)} unknown field(s)")

    if directory != "archive" and RECORD_DIRECTORIES.get(directory) != record_type:
        errors.append(f"{label} record type does not match its directory")

    if record.get("schema_version") != 1 or isinstance(record.get("schema_version"), bool):
        errors.append(f"{label} field 'schema_version' must equal integer 1")

    record_id = record.get("id")
    expected_prefix = TYPE_PREFIX[record_type]
    if not isinstance(record_id, str) or not ID_RE.fullmatch(record_id):
        errors.append(f"{label} field 'id' has an invalid format")
        record_id = None
    elif not record_id.startswith(expected_prefix + "-"):
        errors.append(f"{label} field 'id' does not match its record type")
    elif path.stem != record_id:
        errors.append(f"{label} filename does not match its record id")

    created = parse_timestamp(record.get("created_at"), label, "created_at", errors)
    updated = parse_timestamp(record.get("updated_at"), label, "updated_at", errors)
    if created is not None and updated is not None and updated < created:
        errors.append(f"{label} field 'updated_at' predates 'created_at'")

    if record.get("activation") != "none":
        errors.append(f"{label} must remain inactive with activation='none'")
    if record.get("trusted_as_instruction") is not False:
        errors.append(f"{label} must set trusted_as_instruction=false")
    if record.get("grants_authority") is not False:
        errors.append(f"{label} must set grants_authority=false")
    enum_value(record, "privacy_class", ENUMS["privacy_class"], label, errors)
    enum_value(record, "managed_by", ENUMS["managed_by"], label, errors)
    if not isinstance(record.get("pinned"), bool):
        errors.append(f"{label} field 'pinned' must be Boolean")
    if not nonempty_string(record.get("write_authorization_receipt")):
        errors.append(
            f"{label} field 'write_authorization_receipt' must be a nonempty string"
        )

    if "tags" in record:
        tags = string_list(record["tags"], label, "tags", errors)
        if tags and (len(tags) != len(set(tags)) or any(not TAG_RE.fullmatch(tag) for tag in tags)):
            errors.append(f"{label} field 'tags' must contain unique lowercase slugs")

    return record_id


def validate_observation(record: dict[str, Any], label: str, errors: list[str]) -> None:
    enum_value(record, "signal", ENUMS["signal"], label, errors)
    enum_value(record, "known_scope", ENUMS["known_scope"], label, errors)
    enum_value(record, "status", ENUMS["observation_status"], label, errors)
    for field in ("observable_behavior", "outcome"):
        if not nonempty_string(record.get(field)):
            errors.append(f"{label} field {field!r} must be a nonempty string")
    source_snapshot = record.get("source_skill_snapshot")
    if not isinstance(source_snapshot, dict) or set(source_snapshot) != {
        "skill",
        "version",
        "snapshot",
    }:
        errors.append(
            f"{label} field 'source_skill_snapshot' must contain exactly skill, version, and snapshot"
        )
    else:
        if not nonempty_string(source_snapshot["skill"]):
            errors.append(
                f"{label} source_skill_snapshot field 'skill' must be a nonempty string"
            )
        version = source_snapshot["version"]
        if version is not None and (
            not isinstance(version, str) or not SEMVER_RE.fullmatch(version)
        ):
            errors.append(
                f"{label} source_skill_snapshot field 'version' must be SemVer or null"
            )
        snapshot = source_snapshot["snapshot"]
        if snapshot is not None and not nonempty_string(snapshot):
            errors.append(
                f"{label} source_skill_snapshot field 'snapshot' must be a nonempty string or null"
            )
    string_list(record.get("competing_explanations"), label, "competing_explanations", errors)
    if "responsible_rule" in record and not nonempty_string(record["responsible_rule"]):
        errors.append(f"{label} field 'responsible_rule' must be a nonempty string")


def validate_candidate(record: dict[str, Any], label: str, errors: list[str]) -> None:
    string_list(record.get("observation_ids"), label, "observation_ids", errors, nonempty=True)
    for field in (
        "candidate_behavior",
        "canonical_owner_hypothesis",
        "root_cause",
        "narrowest_scope",
        "current_rule",
    ):
        if not nonempty_string(record.get(field)):
            errors.append(f"{label} field {field!r} must be a nonempty string")
    for field in (
        "same_scope_conflicts",
        "counterevidence",
        "preserved_invariants",
        "regression_risks",
        "claimed_generality_axes",
    ):
        string_list(record.get(field), label, field, errors)
    test_cases = record.get("test_cases")
    required_cases = {"positive", "nearest_negative", "no_authority"}
    if not isinstance(test_cases, dict) or set(test_cases) != required_cases:
        errors.append(f"{label} field 'test_cases' must contain exactly the three required cases")
    elif any(not nonempty_string(test_cases[key]) for key in required_cases):
        errors.append(f"{label} field 'test_cases' contains an empty case")
    eligibility = enum_value(
        record, "promotion_eligibility", ENUMS["promotion_eligibility"], label, errors
    )
    status = enum_value(record, "status", ENUMS["candidate_status"], label, errors)
    if eligibility == "ready-for-review" and status != "supported":
        errors.append(f"{label} ready-for-review eligibility requires supported status")


def validate_evaluation(record: dict[str, Any], label: str, errors: list[str]) -> None:
    for field in ("candidate_id", "baseline_snapshot", "candidate_snapshot", "evaluator"):
        if not nonempty_string(record.get(field)):
            errors.append(f"{label} field {field!r} must be a nonempty string")
    hashes = string_list(record.get("output_hashes"), label, "output_hashes", errors)
    if any(not SHA256_RE.fullmatch(value) for value in hashes):
        errors.append(f"{label} field 'output_hashes' contains an invalid SHA-256 receipt")
    if not isinstance(record.get("holdout_touched"), bool):
        errors.append(f"{label} field 'holdout_touched' must be Boolean")
    status_value = enum_value(record, "status", ENUMS["evaluation_status"], label, errors)
    verdict = enum_value(
        record, "verdict", ENUMS["evaluation_verdict"], label, errors
    )
    if record.get("holdout_touched") is True and status_value == "completed":
        errors.append(f"{label} touched holdout must remain exploratory or invalidated")
    if verdict == "supports":
        if record.get("baseline_snapshot") == record.get("candidate_snapshot"):
            errors.append(f"{label} supporting verdict requires distinct baseline and candidate snapshots")
        if not hashes:
            errors.append(f"{label} supporting verdict requires at least one output hash")

    cases = record.get("cases")
    if not isinstance(cases, list) or not cases:
        errors.append(f"{label} field 'cases' must be a nonempty case array")
        return
    roles: set[str] = set()
    case_ids: set[str] = set()
    case_results: list[str] = []
    for index, case in enumerate(cases, start=1):
        case_label = f"{label} case #{index}"
        if not isinstance(case, dict):
            errors.append(f"{case_label} must be an object")
            continue
        expected_fields = {"id", "role", "result", "notes"}
        if case.get("role") == "generality":
            expected_fields.add("axis")
        elif case.get("role") == "preserved-invariant":
            expected_fields.add("invariant")
        if set(case) != expected_fields:
            errors.append(
                f"{case_label} has fields inconsistent with its evaluation role"
            )
            continue
        if not nonempty_string(case["id"]):
            errors.append(f"{case_label} field 'id' must be a nonempty string")
        elif case["id"] in case_ids:
            errors.append(f"{case_label} duplicates another local case id")
        else:
            case_ids.add(case["id"])
        role = case["role"]
        if role not in ENUMS["evaluation_role"]:
            errors.append(f"{case_label} field 'role' has a disallowed value")
        else:
            roles.add(role)
        if case["result"] not in ENUMS["evaluation_result"]:
            errors.append(f"{case_label} field 'result' has a disallowed value")
        else:
            case_results.append(case["result"])
        if not nonempty_string(case["notes"]):
            errors.append(f"{case_label} field 'notes' must be a nonempty string")
        if case["role"] == "generality" and not nonempty_string(case.get("axis")):
            errors.append(f"{case_label} field 'axis' must be a nonempty string")
        if case["role"] == "preserved-invariant" and not nonempty_string(
            case.get("invariant")
        ):
            errors.append(f"{case_label} field 'invariant' must be a nonempty string")
    required_roles = {"originating", "nearest-negative", "no-authority"}
    missing_roles = required_roles - roles
    if missing_roles:
        errors.append(f"{label} field 'cases' is missing {len(missing_roles)} required role(s)")
    if verdict == "supports":
        if status_value != "completed":
            errors.append(f"{label} supporting verdict requires completed status")
        if case_results and any(result != "pass" for result in case_results):
            errors.append(f"{label} supporting verdict requires every case to pass")


def validate_decision(record: dict[str, Any], label: str, errors: list[str]) -> None:
    if not nonempty_string(record.get("candidate_id")):
        errors.append(f"{label} field 'candidate_id' must be a nonempty string")
    string_list(record.get("evidence_ids"), label, "evidence_ids", errors, nonempty=True)
    decision = enum_value(record, "decision", ENUMS["decision"], label, errors)
    action_scope = enum_value(
        record,
        "recorded_action_scope",
        ENUMS["recorded_action_scope"],
        label,
        errors,
    )
    if (
        decision is not None
        and action_scope is not None
        and action_scope not in DECISION_ACTION_SCOPES[decision]
    ):
        errors.append(
            f"{label} decision is incompatible with recorded_action_scope"
        )
    enum_value(record, "status", ENUMS["decision_status"], label, errors)
    if not nonempty_string(record.get("rationale")):
        errors.append(f"{label} field 'rationale' must be a nonempty string")
    if "supersedes_decision_id" in record and not nonempty_string(record["supersedes_decision_id"]):
        errors.append(f"{label} field 'supersedes_decision_id' must be a nonempty string")


def validate_receipt(record: dict[str, Any], label: str, errors: list[str]) -> None:
    enum_value(record, "event", ENUMS["receipt_event"], label, errors)
    string_list(record.get("subject_ids"), label, "subject_ids", errors, nonempty=True)
    enum_value(record, "outcome", ENUMS["receipt_outcome"], label, errors)
    enum_value(record, "status", ENUMS["receipt_status"], label, errors)
    for field in ("source_snapshot", "details"):
        if not nonempty_string(record.get(field)):
            errors.append(f"{label} field {field!r} must be a nonempty string")


def validate_references(
    indexed: dict[str, tuple[str, dict[str, Any], str]], errors: list[str]
) -> None:
    supporting_evaluations: dict[str, set[str]] = {}
    for record_id, (record_type, record, label) in indexed.items():
        if record_type == "observation":
            continue
        if record_type == "candidate":
            for index, reference in enumerate(record.get("observation_ids", []), start=1):
                target = indexed.get(reference)
                if target is None or target[0] != "observation":
                    errors.append(f"{label} has unresolved observation reference #{index}")
        elif record_type == "evaluation":
            reference = record.get("candidate_id")
            target = indexed.get(reference)
            if target is None or target[0] != "candidate":
                errors.append(f"{label} has an unresolved candidate reference")
            elif (
                record.get("status") == "completed"
                and record.get("verdict") == "supports"
            ):
                cases = record.get("cases", [])
                valid_cases = [case for case in cases if isinstance(case, dict)]
                required_roles = {"originating", "nearest-negative", "no-authority"}
                passed_roles = {
                    case.get("role")
                    for case in valid_cases
                    if case.get("result") == "pass"
                }
                candidate = target[1]
                covered_axes = {
                    case.get("axis")
                    for case in valid_cases
                    if case.get("role") == "generality"
                    and case.get("result") == "pass"
                    and nonempty_string(case.get("axis"))
                }
                missing_axes = set(candidate.get("claimed_generality_axes", [])) - covered_axes
                if missing_axes:
                    errors.append(
                        f"{label} supporting evaluation is missing "
                        f"{len(missing_axes)} claimed generality axis case(s)"
                    )
                conflict_missing = bool(candidate.get("same_scope_conflicts")) and (
                    "conflict" not in passed_roles
                )
                if conflict_missing:
                    errors.append(
                        f"{label} supporting evaluation lacks a passing conflict case"
                    )
                covered_invariants = {
                    case.get("invariant")
                    for case in valid_cases
                    if case.get("role") == "preserved-invariant"
                    and case.get("result") == "pass"
                    and nonempty_string(case.get("invariant"))
                }
                missing_invariants = set(candidate.get("preserved_invariants", [])) - covered_invariants
                if missing_invariants:
                    errors.append(
                        f"{label} supporting evaluation is missing "
                        f"{len(missing_invariants)} preserved invariant case(s)"
                    )
                if (
                    required_roles <= passed_roles
                    and not missing_axes
                    and not conflict_missing
                    and not missing_invariants
                    and record.get("holdout_touched") is False
                    and len(valid_cases) == len(cases)
                    and all(case.get("result") == "pass" for case in valid_cases)
                ):
                    supporting_evaluations.setdefault(reference, set()).add(record_id)
        elif record_type == "decision":
            reference = record.get("candidate_id")
            target = indexed.get(reference)
            if target is None or target[0] != "candidate":
                errors.append(f"{label} has an unresolved candidate reference")
            for index, evidence_id in enumerate(record.get("evidence_ids", []), start=1):
                evidence = indexed.get(evidence_id)
                if evidence is None or evidence[0] not in {"observation", "evaluation"}:
                    errors.append(f"{label} has unresolved evidence reference #{index}")
            if "supersedes_decision_id" in record:
                superseded = indexed.get(record["supersedes_decision_id"])
                if superseded is None or superseded[0] != "decision":
                    errors.append(f"{label} has an unresolved superseded-decision reference")
                elif record["supersedes_decision_id"] == record_id:
                    errors.append(f"{label} cannot supersede itself")
        elif record_type == "receipt":
            for index, subject_id in enumerate(record.get("subject_ids", []), start=1):
                if subject_id not in indexed or subject_id == record_id:
                    errors.append(f"{label} has unresolved subject reference #{index}")

    for _, (record_type, record, label) in indexed.items():
        if record_type == "candidate":
            has_support = bool(supporting_evaluations.get(record.get("id")))
            if not has_support and record.get("promotion_eligibility") == "ready-for-review":
                errors.append(f"{label} ready-for-review state lacks a supporting completed evaluation")
            elif not has_support and record.get("status") == "supported":
                errors.append(f"{label} supported state lacks a supporting completed evaluation")
        elif (
            record_type == "decision"
            and record.get("decision") == "approve-promotion"
            and record.get("status") == "recorded"
        ):
            reference = record.get("candidate_id")
            target = indexed.get(reference)
            if target is None or target[0] != "candidate":
                continue
            candidate = target[1]
            if (
                candidate.get("status") != "supported"
                or candidate.get("promotion_eligibility") != "ready-for-review"
            ):
                errors.append(f"{label} approval requires a supported ready-for-review candidate")
            evidence_ids = set(record.get("evidence_ids", []))
            if not (evidence_ids & supporting_evaluations.get(reference, set())):
                errors.append(
                    f"{label} approval must cite a supporting completed evaluation"
                )


def validate_project(project_root: Path) -> list[str]:
    errors: list[str] = []
    try:
        root_info = project_root.stat()
    except OSError:
        return ["explicit project root does not exist or is inaccessible"]
    if not stat.S_ISDIR(root_info.st_mode):
        return ["explicit project root is not a directory"]

    evolution_root, paths = discover_records(project_root, errors)
    if evolution_root is None:
        return errors

    indexed: dict[str, tuple[str, dict[str, Any], str]] = {}
    validators = {
        "observation": validate_observation,
        "candidate": validate_candidate,
        "evaluation": validate_evaluation,
        "decision": validate_decision,
        "receipt": validate_receipt,
    }
    directory_counts: dict[str, int] = {}
    for directory, path in paths:
        directory_counts[directory] = directory_counts.get(directory, 0) + 1
        label = f"{directory} record #{directory_counts[directory]}"
        record = load_record(path, label, errors)
        if record is None:
            continue
        record_id = validate_common(record, path, directory, label, errors)
        record_type = record.get("record_type")
        if record_type in validators:
            validators[record_type](record, label, errors)
        if record_id is not None and record_type in validators:
            if record_id in indexed:
                errors.append(f"{label} duplicates another project evolution id")
            else:
                indexed[record_id] = (record_type, record, label)

    validate_references(indexed, errors)
    return errors


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate inactive project-local STAR Writing evolution records."
    )
    parser.add_argument(
        "--project-root",
        required=True,
        type=Path,
        help="explicit project root containing optional .star-writing/evolution state",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    project_root = args.project_root.expanduser().resolve(strict=False)
    errors = validate_project(project_root)
    if errors:
        print(f"Project evolution validation failed with {len(errors)} error(s):", file=sys.stderr)
        for index, error in enumerate(errors, start=1):
            print(f"  {index}. {error}", file=sys.stderr)
        return 1

    state = project_root / ".star-writing" / "evolution"
    if not state.exists():
        print("Project evolution state is absent; validation passed.")
        return 0
    record_count = sum(
        1
        for directory in ALLOWED_DIRECTORIES
        if (state / directory).is_dir()
        for path in (state / directory).iterdir()
        if path.is_file() and path.suffix == ".json"
    )
    print(f"Validated {record_count} inactive project evolution record(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
