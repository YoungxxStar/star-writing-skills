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
ALLOWED_MODES = PAPER_MODES
CONTROLLER_MODES = {
    "star-writing": PAPER_MODES,
    "star-writing-start": {"audit"},
    "star-writing-frame": {"explore", "converge", "audit", "revise"},
    "star-writing-literature": {"audit", "revise"},
    "star-writing-method": {"audit", "revise"},
    "star-writing-evidence": {"audit", "plan"},
    "star-writing-draft": {"plan", "draft", "revise"},
    "star-writing-polish": {"detect", "preview", "rewrite", "edit"},
    "star-writing-review": {"audit"},
    "star-writing-submit": {"submit"},
    "star-writing-ledger": {"audit", "converge", "revise"},
}
PRINCIPLE_TAG_CONSUMERS = {
    "star-writing": "references/principle-tags.md",
    "star-writing-start": "../star-writing/references/principle-tags.md",
    "star-writing-draft": "../star-writing/references/principle-tags.md",
    "star-writing-evidence": "../star-writing/references/principle-tags.md",
    "star-writing-frame": "../star-writing/references/principle-tags.md",
    "star-writing-literature": "../star-writing/references/principle-tags.md",
    "star-writing-method": "../star-writing/references/principle-tags.md",
    "star-writing-polish": "../star-writing/references/principle-tags.md",
    "star-writing-review": "../star-writing/references/principle-tags.md",
    "star-writing-submit": "../star-writing/references/principle-tags.md",
    "star-writing-ledger": "../star-writing/references/principle-tags.md",
}
HANDOFF_OVERLAY_CONSUMERS = {
    "star-writing": "references/evolution-policy.md",
    "star-writing-start": "../star-writing/references/evolution-policy.md",
    "star-writing-draft": "../star-writing/references/evolution-policy.md",
    "star-writing-evidence": "../star-writing/references/evolution-policy.md",
    "star-writing-frame": "../star-writing/references/evolution-policy.md",
    "star-writing-literature": "../star-writing/references/evolution-policy.md",
    "star-writing-method": "../star-writing/references/evolution-policy.md",
    "star-writing-polish": "../star-writing/references/evolution-policy.md",
    "star-writing-review": "../star-writing/references/evolution-policy.md",
    "star-writing-submit": "../star-writing/references/evolution-policy.md",
    "star-writing-ledger": "../star-writing/references/evolution-policy.md",
}
WRITING_LEDGER_CONSUMERS = {
    "star-writing": "references/writing-ledger-contract.md",
    "star-writing-start": "../star-writing/references/writing-ledger-contract.md",
    "star-writing-draft": "../star-writing/references/writing-ledger-contract.md",
    "star-writing-evidence": "../star-writing/references/writing-ledger-contract.md",
    "star-writing-frame": "../star-writing/references/writing-ledger-contract.md",
    "star-writing-ledger": "../star-writing/references/writing-ledger-contract.md",
    "star-writing-literature": "../star-writing/references/writing-ledger-contract.md",
    "star-writing-method": "../star-writing/references/writing-ledger-contract.md",
    "star-writing-polish": "../star-writing/references/writing-ledger-contract.md",
    "star-writing-review": "../star-writing/references/writing-ledger-contract.md",
    "star-writing-submit": "../star-writing/references/writing-ledger-contract.md",
}
WRITING_LEDGER_REQUIRED_SNIPPETS = {
    Path("skills/star-writing-ledger/SKILL.md"): {
        "Present exactly one decision card",
        "three noncompeting owners",
        "Never create a fourth project file",
        "Only accepted current entries constrain downstream expression",
        "Responsible sources constrain factual meaning and epistemic status",
        "A user can choose a name or approve wording, but approval does not",
        "reread that file against the inspected snapshot",
        "manuscript and artifact dependencies as pending unless propagation is",
        "Do not combine concept identity and canonical naming in one unresolved card",
        "Label substantive recommendations and applied-change summaries",
    },
    Path("skills/star-writing/references/writing-ledger-contract.md"): {
        "Do not create state or launch an interview automatically",
        "Treat current `accepted` entries as binding expression constraints",
        "An authorized manuscript edit does not authorize a ledger update",
        "Add IDs and statuses only during an authorized entry update",
        "check the exact hidden paths",
        "Only after this exact check may a skill conclude that no project ledger exists",
        "Decision and epistemic status constrain different things",
    },
    Path("skills/star-writing/references/paper-contract.md"): {
        "## Canonical core propositions",
        "Use stable IDs `P-###`",
        "Use propagation status `pending`, `partial`, `checked`, or `out-of-scope`",
    },
    Path("skills/star-writing/references/terminology-and-symbols.md"): {
        "## Concepts and distinctions",
        "Use stable IDs `C-###`, `T-###`, and `S-###`",
        "Manuscript editing alone does not authorize its",
        "Use lock state `unlocked` or `author-locked`",
        "Neutral referent or concept role",
    },
    Path("skills/star-writing/references/state-and-paths.md"): {
        "The first three files form one logical Project Writing Ledger",
        "A ledger update does not",
    },
}
HANDOFF_OVERLAY_REQUIRED_SNIPPETS = {
    Path("skills/star-writing/references/evolution-policy.md"): {
        "STAR Writing does not own a general evolution store",
        "A handoff contains only",
        "Remove manuscript passages, unpublished results, identities",
        "hotskills-selfevol star-writing-skills",
        "Do not recreate its controller inside STAR Writing",
    },
    Path("skills/star-writing/SKILL.md"): {
        "Generic skill evolution is outside STAR Writing",
        "hotskills-selfevol star-writing-skills",
        "Do not interrupt ordinary paper work",
    },
}
REQUIRED_GUARDRAIL_EVAL_IDS = {
    "paper-start-orientation",
    "focused-task-bypasses-start",
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
    "interactive-writing-ledger-convergence",
    "authorized-writing-ledger-update",
    "legacy-writing-ledger-compatibility",
    "missing-writing-ledger-local-work",
    "stale-writing-ledger-source-conflict",
    "downstream-writing-ledger-consumption",
    "scoped-symbol-identity",
    "concurrent-writing-ledger-update",
    "concurrent-new-ledger-id-allocation",
    "accepted-entry-epistemic-boundary",
    "ledger-continue-is-not-approval",
    "ledger-ok-current-entry-only",
    "ledger-ok-but-corrected-value",
    "ledger-apply-visible-batch-only",
    "ledger-praise-is-not-approval",
}
REQUIRED_START_EVAL_CONTRACTS = {
    "paper-start-orientation": {
        "controller": "star-writing-start",
        "mode": "audit",
        "routes": set(),
        "must": {
            "resolve the canonical paper snapshot and relevant source types from read-only inspection without demanding a discoverable briefing from the user",
            "traverse the complete manuscript in document order and inspect associated artifacts only when they affect a load-bearing claim",
            "return a compact Paper Map covering the research contract, motivation chain, central move, argument spine, claims and evidence, terminology candidates, verification boundaries, and one recommended next route",
            "distinguish manuscript assertions from independently verified implementation, empirical, mathematical, literature, reproducibility, and submission facts",
        },
        "must_not": {
            "edit the manuscript or create project state, a Git change, or an external side effect",
            "execute an authorized downstream revision from the audit-only start controller instead of handing it to the responsible skill",
            "claim complete source verification for material that was not inspected",
            "replace orientation with sentence-level polishing, a generic abstract summary, a directory dump, or a full reviewer report",
        },
    },
    "focused-task-bypasses-start": {
        "controller": "star-writing-method",
        "mode": "audit",
        "routes": set(),
        "must": {
            "bind the equation and implementation to their current snapshots",
            "trace each load-bearing symbol and operation to the named responsible source",
            "report the scoped method mismatch without rebuilding a paper-wide orientation map",
        },
        "must_not": {
            "route the already scoped task through star-writing-start",
            "repeat the paper onboarding workflow or demand a general project briefing",
            "edit the manuscript, implementation, or Writing Ledger during the audit",
        },
    },
    "read-only-discussion": {
        "controller": "star-writing-frame",
        "mode": "audit",
        "routes": set(),
        "must": {
            "bind the review to the current manuscript snapshot",
            "report findings without writing project files",
            "separate framing problems from prose preferences",
        },
        "must_not": {
            "edit the manuscript",
            "create persistent project state without authorization",
            "route the scoped Introduction request through star-writing-start or rebuild a paper-wide Paper Map",
            "rewrite the section as the default response",
        },
    },
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
REQUIRED_HANDOFF_EVAL_CONTRACTS = {
    "evolution-feedback-scope-triage": {
        "controller": "star-writing",
        "mode": "audit",
        "routes": {"star-writing-submit"},
        "must": {
            "reconstruct and classify the positive feedback, dissatisfaction, one-time preference, project fact, and venue claim separately",
            "produce at most a public-safe task-local handoff for a plausible reusable gap without changing persistent source or state",
        },
        "must_not": {
            "infer a universal rule or causal mechanism from praise, silence, one complaint, or one successful output",
            "treat a remembered venue rule as current or store a local signal as a shared skill rule",
        },
    },
    "active-task-evolution-handoff": {
        "controller": "star-writing-evidence",
        "mode": "audit",
        "routes": set(),
        "must": {
            "keep the active evidence controller responsible for the paper deliverable and hand off only a public-safe task-local skill-maintenance question to STAR HotSkills",
            "distinguish a rule defect from execution, information, authority, tool, environment, and project-scope failures using observable evidence",
        },
        "must_not": {
            "silently switch the paper task into evolve mode or modify skill source during the read-only audit",
            "promote a self-discovered method from one successful example",
        },
    },
    "evolution-conflict-authorization-plan": {
        "controller": "star-writing",
        "mode": "plan",
        "routes": {"star-writing-submit"},
        "must": {
            "resolve authority, factual responsibility, applicability, and scope as separate questions",
            "name the likely target owner, dependent writing contracts, positive and negative regressions, and the separate STAR HotSkills action boundary",
        },
        "must_not": {
            "let authorization turn an unverified scientific or venue claim into fact",
            "edit, commit, install, push, or release in plan mode",
        },
    },
}

REQUIRED_WRITING_LEDGER_EVAL_CONTRACTS = {
    "research-grounded-terminology-ledger": {
        "controller": "star-writing-ledger",
        "mode": "converge",
        "routes": {"star-writing-literature", "star-writing-method"},
        "must": {
            "verify the established technical usage through field-appropriate sources and use Wikipedia only as a common-usage or source-trail cross-check",
            "resolve concept identity, canonical term, and symbol as separate cards without assigning a stable ID or writing before acceptance",
            "keep project-state persistence and later manuscript propagation as separately authorized actions",
        },
        "must_not": {
            "use Wikipedia alone to support a consequential scientific claim",
            "coin a new label when an established term has the same operational meaning",
            "maintain competing terminology tables as separate sources of truth",
            "write project state or manuscript content during the unresolved convergence turn",
        },
    },
    "interactive-writing-ledger-convergence": {
        "controller": "star-writing-ledger",
        "mode": "converge",
        "routes": {"star-writing-frame", "star-writing-evidence"},
        "must": {
            "present exactly one decision card with one focused question and keep all other candidate entries queued",
            "state the responsible source, meaning boundary, distinction, decision status, epistemic status when applicable, dependencies, and preview-only persistence mode",
            "treat continue, silence, or praise as non-approval and accept only the currently displayed entry after explicit approval",
        },
        "must_not": {
            "write project state, manuscript, Git, installation, or external artifacts",
            "merge distinct concepts or invent missing facts to complete the ledger",
        },
    },
    "authorized-writing-ledger-update": {
        "controller": "star-writing-ledger",
        "mode": "revise",
        "routes": set(),
        "must": {
            "update only the accepted named entry in its single owner file after rereading the current snapshot",
            "if a material supersession requires history and the decision log is not authorized, report it pending; otherwise state that no history entry is required",
            "keep manuscript propagation, Git actions, installation, push, and release separately unauthorized",
        },
        "must_not": {
            "rewrite unrelated ledger entries or use unbounded string replacement",
            "treat approval of this entry as approval of other pending entries",
        },
    },
    "legacy-writing-ledger-compatibility": {
        "controller": "star-writing-ledger",
        "mode": "audit",
        "routes": set(),
        "must": {
            "treat paper-contract.md, terminology-and-symbols.md, and decision-log.md as one logical Writing Ledger with noncompeting owners",
            "read current accepted entries without requiring migration or duplicating definitions",
            "treat an unversioned legacy row as accepted only when it is explicitly canonical or locked, unambiguous, and source-consistent, otherwise queue it for reconciliation",
        },
        "must_not": {
            "create a fourth aggregate writing-ledger.md file",
            "treat modification time or the decision log as authoritative current semantic state",
        },
    },
    "missing-writing-ledger-local-work": {
        "controller": "star-writing-polish",
        "mode": "rewrite",
        "routes": set(),
        "must": {
            "complete the local meaning-preserving rewrite from supplied context without creating project state or launching a ledger interview",
            "keep any needed term choice task-local and preserve repeated technical terminology",
        },
        "must_not": {
            "block a routine edit because no Writing Ledger exists",
            "create .star-writing files or invent a canonical project decision",
        },
    },
    "stale-writing-ledger-source-conflict": {
        "controller": "star-writing-ledger",
        "mode": "audit",
        "routes": {"star-writing-method", "star-writing-evidence"},
        "must": {
            "treat the verified responsible source and latest deliberate author edit as conflict evidence, report the ledger entry task-locally as stale and nonbinding, and return to one reconciliation decision",
            "separate decision status from epistemic claim status and preserve the current task scope",
        },
        "must_not": {
            "blindly obey the ledger or silently overwrite the ledger, manuscript, or implementation",
            "promote a user-approved label into an established scientific claim",
        },
    },
    "downstream-writing-ledger-consumption": {
        "controller": "star-writing-draft",
        "mode": "revise",
        "routes": set(),
        "must": {
            "check the exact hidden ledger paths, freeze the task-relevant accepted projection, and use one canonical expression per referent within scope",
            "preserve distinct concept IDs and exclude provisional, unresolved, superseded, and deprecated expressions from the canonical rewrite unless an explicit epistemic role requires mention",
            "consume the two accepted distinct concepts directly without opening a ledger interaction",
            "route to star-writing-ledger only if an actual material unresolved conflict is found and do not change project state",
        },
        "must_not": {
            "introduce stylistic synonyms for accepted technical terms or collapse distinct concepts with similar names",
            "silently update the ledger as a side effect of manuscript revision",
        },
    },
    "scoped-symbol-identity": {
        "controller": "star-writing-method",
        "mode": "audit",
        "routes": {"star-writing-ledger"},
        "must": {
            "compare referent, type, shape, domain, unit, availability, and scope before deciding whether symbols are identical",
            "allow unambiguous local dummy-index reuse while separating global objects with different semantic contracts",
        },
        "must_not": {
            "merge symbols because their glyphs match or rename them only for stylistic variety",
            "write a canonical symbol entry during a read-only method audit",
        },
    },
    "concurrent-writing-ledger-update": {
        "controller": "star-writing-ledger",
        "mode": "revise",
        "routes": set(),
        "must": {
            "reread the owner file immediately before writing and compare the accepted entry with the inspected snapshot",
            "stop for semantic reconciliation when another writer changed the same entry or its meaning",
        },
        "must_not": {
            "overwrite concurrent work, infer ownership from modification time, or replace the whole ledger file",
            "apply an approved entry to unrelated manuscript or project files",
        },
    },
    "concurrent-new-ledger-id-allocation": {
        "controller": "star-writing-ledger",
        "mode": "revise",
        "routes": set(),
        "must": {
            "keep the task-local candidate on a temporary referent key and reread the owner before allocating an ID",
            "preserve the concurrent new entry and allocate one greater than the namespace's historical maximum after rereading the owner and relevant decision history",
        },
        "must_not": {
            "reserve a stable ID before persistence, fill an ID gap, or reuse an occupied or retired ID",
            "overwrite the concurrent entry, renumber existing entries, or rewrite the whole owner file",
        },
    },
    "accepted-entry-epistemic-boundary": {
        "controller": "star-writing-draft",
        "mode": "revise",
        "routes": set(),
        "must": {
            "treat accepted as the canonical expression decision rather than proof of the proposition",
            "present the exploratory proposition only as a hypothesis, preserve every bounded qualifier, and exclude unsupported or contradicted content from established conclusions",
        },
        "must_not": {
            "turn author acceptance into established evidence or erase the epistemic qualifier",
            "state an unsupported, contradicted, or unresolved accepted proposition as a finding or premise",
        },
    },
    "ledger-continue-is-not-approval": {
        "controller": "star-writing-ledger",
        "mode": "converge",
        "routes": set(),
        "must": {
            "continue the current unresolved card without accepting it or advancing to the queued card",
            "preserve preview-only state and ask at most one decision-changing question",
        },
        "must_not": {
            "write project state or interpret continue as approval, deferment, or apply-all",
            "display a second full decision card while the current card remains unresolved",
        },
    },
    "ledger-ok-current-entry-only": {
        "controller": "star-writing-ledger",
        "mode": "revise",
        "routes": set(),
        "must": {
            "accept and persist only the exact currently displayed entry under the previously stated write boundary",
            "leave undisplayed or queued entries unaccepted and report their dependencies as pending",
        },
        "must_not": {
            "treat OK as approval of the queue, manuscript propagation, Git, installation, push, or release",
            "modify an owner or entry outside the displayed decision",
        },
    },
    "ledger-ok-but-corrected-value": {
        "controller": "star-writing-ledger",
        "mode": "revise",
        "routes": set(),
        "must": {
            "accept the user's corrected value as the current decision and reject the superseded proposal",
            "persist only the corrected value inside the stated owner-file boundary",
        },
        "must_not": {
            "record the original proposal as accepted or expand approval to another entry",
            "propagate the corrected value without separate authorization",
        },
    },
    "ledger-apply-visible-batch-only": {
        "controller": "star-writing-ledger",
        "mode": "revise",
        "routes": set(),
        "must": {
            "apply only the entries already displayed in the explicitly named batch and preserve their individual statuses",
            "leave every hidden, queued, or later entry unchanged",
        },
        "must_not": {
            "interpret apply all as approval of undisplayed decisions or unrelated files",
            "bypass responsible-source or concurrent-snapshot checks for the visible entries",
        },
    },
    "ledger-praise-is-not-approval": {
        "controller": "star-writing-ledger",
        "mode": "converge",
        "routes": set(),
        "must": {
            "treat praise as feedback while keeping the displayed entry unresolved",
            "ask one focused acceptance or revision question without changing persistence state",
        },
        "must_not": {
            "infer acceptance, persistence authority, or approval of queued entries from praise",
            "write project state, manuscript content, or external artifacts",
        },
    },
}
REQUIRED_WRITING_LEDGER_EVAL_PROMPT_MARKERS = {
    "research-grounded-terminology-ledger": {
        "No canonical form has been accepted yet",
        "Do not write any file until I accept the current card",
    },
    "interactive-writing-ledger-convergence": {"Preview only"},
    "authorized-writing-ledger-update": {
        "authorize updating only its named Writing Ledger owner file"
    },
    "legacy-writing-ledger-compatibility": {"Do not modify or migrate anything"},
    "missing-writing-ledger-local-work": {"no .star-writing directory"},
    "stale-writing-ledger-source-conflict": {"Audit only"},
    "downstream-writing-ledger-consumption": {"Do not modify project state"},
    "scoped-symbol-identity": {"Do not edit files"},
    "concurrent-writing-ledger-update": {"another writer changed the same"},
    "concurrent-new-ledger-id-allocation": {
        "another writer has since added T-008"
    },
    "accepted-entry-epistemic-boundary": {"Do not edit project state"},
    "ledger-continue-is-not-approval": {"Current user reply: continue"},
    "ledger-ok-current-entry-only": {"Current user reply: OK"},
    "ledger-ok-but-corrected-value": {
        "previously verified, source-consistent rendering within the same meaning boundary",
        "OK, but use Y",
    },
    "ledger-apply-visible-batch-only": {"Current user reply: apply all"},
    "ledger-praise-is-not-approval": {"Current user reply: this is excellent"},
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
    "HPC or workspace path": re.compile(
        r"/(?:cephfs|rds|scratch|workspaces)/"
    ),
    "literal POSIX user home": re.compile(
        r"/(?:home|users|Users)/[^/\s`'\"]+/"
    ),
    "literal Windows user home": re.compile(
        r"[A-Za-z]:\\Users\\[^\\\s`'\"]+\\"
    ),
}


def reject_duplicate_json_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_nonfinite_json(value: str) -> None:
    raise ValueError(f"non-finite JSON value: {value}")


def load_json(path: Path, errors: list[str]) -> Any:
    try:
        return json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=reject_duplicate_json_keys,
            parse_constant=reject_nonfinite_json,
        )
    except FileNotFoundError:
        errors.append(f"missing file: {path.relative_to(ROOT)}")
    except json.JSONDecodeError as exc:
        errors.append(
            f"invalid JSON in {path.relative_to(ROOT)}: "
            f"line {exc.lineno}, column {exc.colno}: {exc.msg}"
        )
    except ValueError as exc:
        errors.append(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")
    return None


def parse_frontmatter_text(
    text: str, label: str, errors: list[str]
) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        errors.append(f"missing YAML frontmatter: {label}")
        return {}

    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        errors.append(f"unterminated YAML frontmatter: {label}")
        return {}

    metadata: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        if key in metadata:
            errors.append(f"duplicate frontmatter field: {label}")
            continue
        metadata[key] = value.strip().strip("\"'")
    return metadata


def parse_frontmatter(path: Path, errors: list[str]) -> dict[str, str]:
    return parse_frontmatter_text(
        path.read_text(encoding="utf-8"), str(path.relative_to(ROOT)), errors
    )


def safe_relative_label(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


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
        "evolution-handoff": set(HANDOFF_OVERLAY_CONSUMERS),
        "writing-ledger": set(WRITING_LEDGER_CONSUMERS),
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

    for skill_name, expected_link in HANDOFF_OVERLAY_CONSUMERS.items():
        skill_file = SKILLS_DIR / skill_name / "SKILL.md"
        if not skill_file.is_file():
            errors.append(f"missing skill file for evolution handoff: {skill_name}")
            continue
        if expected_link not in skill_file.read_text(encoding="utf-8"):
            errors.append(
                f"{skill_name} does not consume the shared evolution handoff"
            )

    for skill_name, expected_link in WRITING_LEDGER_CONSUMERS.items():
        skill_file = SKILLS_DIR / skill_name / "SKILL.md"
        if not skill_file.is_file():
            errors.append(f"missing skill file for Writing Ledger contract: {skill_name}")
            continue
        if expected_link not in skill_file.read_text(encoding="utf-8"):
            errors.append(
                f"{skill_name} does not consume the shared Writing Ledger contract"
            )

    for relative, snippets in WRITING_LEDGER_REQUIRED_SNIPPETS.items():
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"missing Writing Ledger contract file: {relative}")
            continue
        text = re.sub(r"\s+", " ", path.read_text(encoding="utf-8"))
        for snippet in sorted(snippets):
            if snippet not in text:
                errors.append(
                    f"Writing Ledger contract file {relative} is missing a "
                    f"required invariant: {snippet!r}"
                )

    for relative, snippets in HANDOFF_OVERLAY_REQUIRED_SNIPPETS.items():
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"missing evolution handoff contract file: {relative}")
            continue
        text = re.sub(r"\s+", " ", path.read_text(encoding="utf-8"))
        for snippet in sorted(snippets):
            if snippet not in text:
                errors.append(
                    f"evolution handoff contract file {relative} is missing a "
                    f"required invariant: {snippet!r}"
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
            line = text.count("\n", 0, match.start()) + 1
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(
                    f"filesystem-external Markdown link in "
                    f"{safe_relative_label(path)}:{line}"
                )
            else:
                if not resolved.exists():
                    errors.append(
                        f"broken Markdown link in {safe_relative_label(path)}:{line}"
                    )


def validate_path_portability(errors: list[str]) -> None:
    validator = Path(__file__).resolve()
    for path in sorted(ROOT.rglob("*")):
        if path.is_symlink():
            if path.suffix in PORTABLE_TEXT_SUFFIXES:
                errors.append(
                    f"symlinked portable-text file is not allowed: "
                    f"{safe_relative_label(path)}"
                )
            continue
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
                    f"{label} in {safe_relative_label(path)}:{line}"
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

    for case_id, contract in REQUIRED_START_EVAL_CONTRACTS.items():
        case = cases_by_id.get(case_id)
        if case is None:
            errors.append(f"missing required start-routing eval: {case_id}")
            continue

        if case.get("expected_controller") != contract["controller"]:
            errors.append(
                f"start-routing eval {case_id} must use controller "
                f"{contract['controller']!r}"
            )
        if case.get("expected_mode") != contract["mode"]:
            errors.append(
                f"start-routing eval {case_id} must use mode {contract['mode']!r}"
            )
        routes = case.get("expected_routes", [])
        if isinstance(routes, list) and set(routes) != contract["routes"]:
            errors.append(f"start-routing eval {case_id} has the wrong route contract")
        for field in ("must", "must_not"):
            values = case.get(field, [])
            if not isinstance(values, list):
                continue
            actual_values = set(values)
            missing_values = sorted(contract[field] - actual_values)
            if missing_values:
                errors.append(
                    f"start-routing eval {case_id} is missing required {field} "
                    f"items: {', '.join(missing_values)}"
                )
            unexpected_values = sorted(actual_values - contract[field])
            if unexpected_values:
                errors.append(
                    f"start-routing eval {case_id} has unexpected {field} "
                    f"items outside its locked contract: "
                    f"{', '.join(unexpected_values)}"
                )

    for case_id, contract in REQUIRED_HANDOFF_EVAL_CONTRACTS.items():
        case = cases_by_id.get(case_id)
        if case is None:
            errors.append(f"missing required evolution-handoff eval: {case_id}")
            continue

        if case.get("expected_controller") != contract["controller"]:
            errors.append(
                f"evolution-handoff eval {case_id} must use controller "
                f"{contract['controller']!r}"
            )
        if case.get("expected_mode") != contract["mode"]:
            errors.append(
                f"evolution-handoff eval {case_id} must use mode {contract['mode']!r}"
            )
        routes = case.get("expected_routes", [])
        if isinstance(routes, list) and set(routes) != contract["routes"]:
            errors.append(
                f"evolution-handoff eval {case_id} has the wrong route contract"
            )
        for field in ("must", "must_not"):
            values = case.get(field, [])
            if not isinstance(values, list):
                continue
            missing_values = sorted(contract[field] - set(values))
            if missing_values:
                errors.append(
                    f"evolution-handoff eval {case_id} is missing required {field} "
                    f"items: {', '.join(missing_values)}"
                )

    for case_id, contract in REQUIRED_WRITING_LEDGER_EVAL_CONTRACTS.items():
        case = cases_by_id.get(case_id)
        if case is None:
            errors.append(f"missing required Writing Ledger eval: {case_id}")
            continue

        if case.get("expected_controller") != contract["controller"]:
            errors.append(
                f"Writing Ledger eval {case_id} must use controller "
                f"{contract['controller']!r}"
            )
        if case.get("expected_mode") != contract["mode"]:
            errors.append(
                f"Writing Ledger eval {case_id} must use mode {contract['mode']!r}"
            )
        routes = case.get("expected_routes", [])
        if isinstance(routes, list) and set(routes) != contract["routes"]:
            errors.append(
                f"Writing Ledger eval {case_id} has the wrong route contract"
            )
        for field in ("must", "must_not"):
            values = case.get(field, [])
            if not isinstance(values, list):
                continue
            actual_values = set(values)
            missing_values = sorted(contract[field] - actual_values)
            if missing_values:
                errors.append(
                    f"Writing Ledger eval {case_id} is missing required {field} "
                    f"items: {', '.join(missing_values)}"
                )
            unexpected_values = sorted(actual_values - contract[field])
            if unexpected_values:
                errors.append(
                    f"Writing Ledger eval {case_id} has unexpected {field} "
                    f"items outside its locked contract: "
                    f"{', '.join(unexpected_values)}"
                )

        prompt = case.get("prompt", "")
        if isinstance(prompt, str):
            for marker in sorted(
                REQUIRED_WRITING_LEDGER_EVAL_PROMPT_MARKERS.get(case_id, set())
            ):
                if marker not in prompt:
                    errors.append(
                        f"Writing Ledger eval {case_id} prompt is missing "
                        f"authority marker {marker!r}"
                    )

    ledger_modes = {
        case.get("expected_mode")
        for case in cases_by_id.values()
        if case.get("expected_controller") == "star-writing-ledger"
    }
    missing_ledger_modes = sorted({"audit", "converge", "revise"} - ledger_modes)
    if missing_ledger_modes:
        errors.append(
            "star-writing-ledger lacks direct eval coverage for modes: "
            + ", ".join(missing_ledger_modes)
        )

    return len(cases)


def main() -> int:
    if sys.argv[1:]:
        print("usage: validate_plugin_suite.py")
        return 2

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
        f"{len(skill_names)} skills and {spec_count} behavioral specifications "
        "structurally valid, all local Markdown links resolved, no machine-specific paths "
        "detected. "
        "No behavioral executions were performed."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
