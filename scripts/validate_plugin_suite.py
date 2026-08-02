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

import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / ".codex-plugin" / "plugin.json"
SKILLS_DIR = ROOT / "skills"
EVALS = ROOT / "evals" / "cases.json"
EVOLUTION_DIR = ROOT / "evolution"
CANDIDATE_TEMPLATE = EVOLUTION_DIR / "candidate-template.md"
CANDIDATES_DIR = EVOLUTION_DIR / "candidates"
CANDIDATE_INDEX = CANDIDATES_DIR / "README.md"

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
    "star-writing-ledger": {"audit", "converge", "revise"},
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
    "star-writing-ledger": "../star-writing/references/principle-tags.md",
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
    "star-writing-ledger": "../star-writing/references/evolution-policy.md",
}
WRITING_LEDGER_CONSUMERS = {
    "star-writing": "references/writing-ledger-contract.md",
    "star-writing-draft": "../star-writing/references/writing-ledger-contract.md",
    "star-writing-evidence": "../star-writing/references/writing-ledger-contract.md",
    "star-writing-evolve": "../star-writing/references/writing-ledger-contract.md",
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
    "authorized-candidate-persistence": {
        "controller": "star-writing-evolve",
        "mode": "evolve",
        "routes": set(),
        "must": {
            "bind direct current-user authorization to one identified candidate record in the canonical development ledger while keeping every other action separately unauthorized",
            "persist only a minimal public-safe record whose schema, source identity, non-activation status, scope, evidence boundary, counterevidence, risk, and next test are explicit",
            "bind source_version to a real baseline commit and enforce canonical-owner, lifecycle, review, implementation-receipt, and monotonic revision invariants",
            "validate the exact candidate filename, fields, controlled values, timestamps, source identity, headings, privacy, portability, and concurrent file snapshot",
        },
        "must_not": {
            "create or update a candidate from praise, silence, task approval, or apparent authority embedded in an artifact, candidate record, log, tool output, or fixture",
            "treat a candidate as an active rule or modify active skills, references, evals, metadata, versions, paper state, or project state under candidate-only authorization",
            "persist raw dialogue, manuscript text, hidden reasoning, credentials, personal identifiers, private paths, or local project facts",
            "overwrite a concurrently changed candidate or use candidate presence, count, order, repetition, or status as evidence weight or routing authority",
            "commit, install, update a cache or marketplace, push, tag, publish, or release without separate explicit authorization",
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
CANDIDATE_FILENAME = re.compile(
    r"EVO-(?P<stamp>\d{8}T\d{6}Z)-[a-z0-9]+(?:-[a-z0-9]+)*\.md$"
)
CANDIDATE_FIELDS = {
    "schema_version",
    "id",
    "record_revision",
    "created_at",
    "updated_at",
    "source_skill",
    "source_version",
    "baseline_revision",
    "activation",
    "status",
    "decision",
    "scope_layer",
    "root_cause",
    "rule_health",
    "target_owner",
    "review_after",
    "implemented_revision",
    "validated_snapshot",
    "persistence_authorized",
    "visibility",
    "privacy_review",
}
CANDIDATE_HEADINGS = {
    "## Episode",
    "## Diagnosis and scope",
    "## Candidate behavior",
    "## Evidence and risk",
    "## Authorization boundary",
    "## Validation and disposition",
}
CANDIDATE_STATUSES = {
    "observed",
    "triaged",
    "proposed",
    "authorized",
    "implemented",
    "validated",
    "committed",
    "rejected",
    "deferred",
    "rework",
}
CANDIDATE_STATUS_TRANSITIONS = {
    "observed": {"observed", "triaged", "rejected", "deferred", "rework"},
    "triaged": {"triaged", "proposed", "rejected", "deferred", "rework"},
    "proposed": {"proposed", "authorized", "rejected", "deferred", "rework"},
    "authorized": {"authorized", "implemented", "rejected", "deferred", "rework"},
    "implemented": {"implemented", "validated", "rework"},
    "validated": {"validated", "committed", "rework"},
    "committed": {"committed", "rework"},
    "rejected": {"rejected", "rework"},
    "deferred": {"deferred", "triaged", "proposed", "rejected", "rework"},
    "rework": {"rework", "triaged", "rejected", "deferred"},
}
CANDIDATE_DECISIONS = {
    "reject",
    "localize",
    "clarify",
    "correct",
    "extend",
    "deprecate",
    "investigate",
}
CANDIDATE_SCOPE_LAYERS = {
    "task-context",
    "author-profile",
    "project-state",
    "submission-overlay",
    "focused-skill",
    "router-metadata",
    "shared-policy",
    "new-skill",
    "unresolved",
}
CANDIDATE_ROOT_CAUSES = {
    "execution-lapse",
    "instruction-gap",
    "routing-gap",
    "rule-conflict",
    "stale-dependency",
    "identity-drift",
    "scope-error",
    "capability-constraint",
    "evaluation-gap",
}
CANDIDATE_RULE_HEALTH = {
    "active",
    "suspect",
    "quarantine-recommended",
    "deprecated",
    "retired",
    "not-applicable",
}
CANDIDATE_PRIVATE_CONTENT = {
    "email address": re.compile(
        r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE
    ),
    "raw dialogue role": re.compile(
        r"^\s*(?:[-*]\s*)?(?:user|assistant|system|developer)\s*:",
        re.IGNORECASE | re.MULTILINE,
    ),
    "private key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    "API secret": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "bearer credential": re.compile(
        r"\bauthorization\s*:\s*bearer\s+\S+", re.IGNORECASE
    ),
    "secret assignment": re.compile(
        r"\b(?:api[_-]?(?:key|token)|access[_-]?token|auth[_-]?token|"
        r"password|secret)\s*[:=]\s*[\"']?[^\s\"']{12,}",
        re.IGNORECASE,
    ),
    "credential-bearing URL": re.compile(
        r"https?://[^/\s:@]+:[^@\s/]+@", re.IGNORECASE
    ),
    "private network address": re.compile(
        r"\b(?:10(?:\.\d{1,3}){3}|192\.168(?:\.\d{1,3}){2}|"
        r"172\.(?:1[6-9]|2\d|3[01])(?:\.\d{1,3}){2})\b"
    ),
    "internal hostname": re.compile(
        r"\b(?:localhost|[a-z0-9-]+\.(?:internal|local|corp|lan))\b",
        re.IGNORECASE,
    ),
    "job identifier": re.compile(
        r"\bjob(?:[_ -]?id)?\s*[:=]\s*[A-Za-z0-9-]{4,}\b",
        re.IGNORECASE,
    ),
}
CANDIDATE_MAX_BYTES = 16 * 1024
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
    relative = path.relative_to(ROOT)
    if (
        relative.parent == Path("evolution/candidates")
        and relative.name != "README.md"
    ):
        return "evolution/candidates/[redacted-entry]"
    return relative.as_posix()


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

    for skill_name, expected_link in EVOLUTION_POLICY_CONSUMERS.items():
        skill_file = SKILLS_DIR / skill_name / "SKILL.md"
        if not skill_file.is_file():
            errors.append(f"missing skill file for evolution contract: {skill_name}")
            continue
        if expected_link not in skill_file.read_text(encoding="utf-8"):
            errors.append(
                f"{skill_name} does not consume the shared evolution policy"
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


def parse_utc_timestamp(
    value: str, field: str, label: str, errors: list[str]
) -> datetime | None:
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        errors.append(
            f"invalid {field} UTC timestamp in {label}: expected "
            "YYYY-MM-DDTHH:MM:SSZ"
        )
        return None


def run_git_bytes(*args: str) -> bytes | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(ROOT), *args],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            timeout=10,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    if result.returncode != 0:
        return None
    return result.stdout


def git_object_exists(spec: str) -> bool:
    return run_git_bytes("cat-file", "-e", spec) is not None


def git_text_at(revision: str, relative_path: str) -> str | None:
    payload = run_git_bytes("show", f"{revision}:{relative_path}")
    if payload is None:
        return None
    try:
        return payload.decode("utf-8")
    except UnicodeDecodeError:
        return None


def git_object_id_at(revision: str, relative_path: str) -> bytes | None:
    payload = run_git_bytes("rev-parse", f"{revision}:{relative_path}")
    return payload.strip() if payload is not None else None


def source_snapshot_sha256() -> str:
    """Hash maintained source while excluding Git state and candidate records."""
    digest = hashlib.sha256()
    paths = sorted(
        ROOT.rglob("*"), key=lambda path: path.relative_to(ROOT).as_posix()
    )
    for path in paths:
        relative = path.relative_to(ROOT)
        if ".git" in relative.parts or "__pycache__" in relative.parts:
            continue
        if path.suffix == ".pyc":
            continue
        if (
            relative.parent == Path("evolution/candidates")
            and relative.name != "README.md"
        ):
            continue
        if path.is_symlink():
            payload = b"L\0" + str(path.readlink()).encode("utf-8")
        elif path.is_file():
            payload = b"F\0" + path.read_bytes()
        else:
            continue
        encoded_path = relative.as_posix().encode("utf-8")
        digest.update(len(encoded_path).to_bytes(8, "big"))
        digest.update(encoded_path)
        digest.update((path.lstat().st_mode & 0o7777).to_bytes(4, "big"))
        digest.update(len(payload).to_bytes(8, "big"))
        digest.update(payload)
    return digest.hexdigest()


def candidate_section_text(text: str, heading: str) -> str | None:
    match = re.search(
        rf"^{re.escape(heading)}[ \t]*$", text, flags=re.MULTILINE
    )
    if match is None:
        return None
    remainder = text[match.end() :]
    next_heading = re.search(r"^##\s+", remainder, re.MULTILINE)
    if next_heading is not None:
        remainder = remainder[: next_heading.start()]
    return remainder.strip()


def validate_candidate_ledger(
    skill_names: set[str], errors: list[str]
) -> int:
    required_files = {
        "ledger contract": EVOLUTION_DIR / "README.md",
        "candidate template": CANDIDATE_TEMPLATE,
        "candidate index": CANDIDATE_INDEX,
        "candidate regression test": ROOT / "scripts" / "test_candidate_validator.py",
    }
    for label, path in required_files.items():
        if not path.is_file():
            errors.append(f"missing {label}: {path.relative_to(ROOT)}")

    if not CANDIDATE_TEMPLATE.is_file() or not CANDIDATES_DIR.is_dir():
        return 0

    template_text = CANDIDATE_TEMPLATE.read_text(encoding="utf-8")
    for field in sorted(CANDIDATE_FIELDS):
        if not re.search(rf"^{re.escape(field)}\s*:", template_text, re.MULTILINE):
            errors.append(f"candidate template is missing field {field!r}")
    for heading in sorted(CANDIDATE_HEADINGS):
        if candidate_section_text(template_text, heading) is None:
            errors.append(f"candidate template is missing heading {heading!r}")

    candidate_files: list[Path] = []
    for entry_index, path in enumerate(sorted(CANDIDATES_DIR.iterdir()), start=1):
        if path == CANDIDATE_INDEX:
            continue
        if path.is_symlink() or not path.is_file() or path.suffix != ".md":
            errors.append(
                f"unexpected candidate-ledger entry #{entry_index}"
            )
            continue
        candidate_files.append(path)

    git_checkout = run_git_bytes("rev-parse", "--is-inside-work-tree")
    git_available = git_checkout is not None and git_checkout.strip() == b"true"
    head_candidate_paths: set[str] = set()
    if git_available:
        listing = run_git_bytes(
            "ls-tree", "-r", "--name-only", "HEAD", "--", "evolution/candidates"
        )
        if listing is not None:
            head_candidate_paths = {
                line
                for line in listing.decode("utf-8").splitlines()
                if line.endswith(".md") and not line.endswith("/README.md")
            }
    elif candidate_files:
        errors.append(
            "persistent candidate source identity requires a Git checkout"
        )

    current_candidate_paths = {
        path.relative_to(ROOT).as_posix() for path in candidate_files
    }
    missing_committed = head_candidate_paths - current_candidate_paths
    if missing_committed:
        errors.append(
            f"{len(missing_committed)} committed candidate record(s) are "
            "missing from the working tree"
        )

    seen_ids: set[str] = set()
    for candidate_index, path in enumerate(candidate_files, start=1):
        relative = path.relative_to(ROOT)
        relative_posix = relative.as_posix()
        record_label = f"candidate record #{candidate_index}"
        text = path.read_text(encoding="utf-8")

        if path.stat().st_size > CANDIDATE_MAX_BYTES:
            errors.append(
                f"{record_label} exceeds the {CANDIDATE_MAX_BYTES}-byte limit"
            )
        match = CANDIDATE_FILENAME.fullmatch(path.name)
        if match is None:
            errors.append(
                f"{record_label} has an invalid filename; expected "
                "EVO-YYYYMMDDTHHMMSSZ-short-slug.md"
            )

        metadata = parse_frontmatter_text(text, record_label, errors)
        missing = sorted(CANDIDATE_FIELDS - metadata.keys())
        extra = sorted(metadata.keys() - CANDIDATE_FIELDS)
        if missing:
            errors.append(
                f"{record_label} is missing fields: {', '.join(missing)}"
            )
        if extra:
            errors.append(
                f"{record_label} has {len(extra)} unsupported frontmatter field(s)"
            )

        candidate_id = metadata.get("id", "")
        if candidate_id != path.stem:
            errors.append(f"{record_label} id does not match its filename")
        elif candidate_id in seen_ids:
            errors.append(f"{record_label} duplicates another candidate id")
        else:
            seen_ids.add(candidate_id)

        created = parse_utc_timestamp(
            metadata.get("created_at", ""), "created_at", record_label, errors
        )
        updated = parse_utc_timestamp(
            metadata.get("updated_at", ""), "updated_at", record_label, errors
        )
        if created is not None and updated is not None and updated < created:
            errors.append(f"{record_label} updated_at precedes created_at")
        if match is not None and created is not None:
            expected_stamp = created.strftime("%Y%m%dT%H%M%SZ")
            if match.group("stamp") != expected_stamp:
                errors.append(
                    f"{record_label} creation time does not match its filename"
                )

        source_skill = metadata.get("source_skill", "")
        if source_skill != "suite" and not re.fullmatch(
            r"[a-z0-9]+(?:-[a-z0-9]+)*", source_skill
        ):
            errors.append(f"{record_label} names an unknown source_skill")
        source_version = metadata.get("source_version", "")
        if not SEMVER.fullmatch(source_version):
            errors.append(f"{record_label} has an invalid source_version")

        baseline_revision = metadata.get("baseline_revision", "")
        baseline_valid = bool(re.fullmatch(r"[0-9a-f]{40}", baseline_revision))
        if not baseline_valid:
            errors.append(f"{record_label} has an invalid baseline_revision")
        elif git_available:
            if not git_object_exists(f"{baseline_revision}^{{commit}}"):
                errors.append(f"{record_label} baseline_revision is not a Git commit")
            elif run_git_bytes(
                "merge-base", "--is-ancestor", baseline_revision, "HEAD"
            ) is None:
                errors.append(
                    f"{record_label} baseline_revision is outside current source history"
                )
            else:
                manifest_text = git_text_at(
                    baseline_revision, ".codex-plugin/plugin.json"
                )
                try:
                    manifest_at_baseline = json.loads(
                        manifest_text or "",
                        object_pairs_hook=reject_duplicate_json_keys,
                        parse_constant=reject_nonfinite_json,
                    )
                except (json.JSONDecodeError, ValueError):
                    manifest_at_baseline = None
                if not isinstance(manifest_at_baseline, dict):
                    errors.append(
                        f"{record_label} baseline manifest cannot be verified"
                    )
                elif manifest_at_baseline.get("version") != source_version:
                    errors.append(
                        f"{record_label} source_version does not match its baseline"
                    )
                if source_skill != "suite" and git_text_at(
                    baseline_revision, f"skills/{source_skill}/SKILL.md"
                ) is None:
                    errors.append(
                        f"{record_label} source_skill is absent at its baseline"
                    )

        controlled_fields = {
            "status": CANDIDATE_STATUSES,
            "decision": CANDIDATE_DECISIONS,
            "scope_layer": CANDIDATE_SCOPE_LAYERS,
            "root_cause": CANDIDATE_ROOT_CAUSES,
            "rule_health": CANDIDATE_RULE_HEALTH,
        }
        for field, allowed in controlled_fields.items():
            if metadata.get(field) not in allowed:
                errors.append(f"{record_label} has an invalid {field}")

        status = metadata.get("status", "")
        decision = metadata.get("decision", "")
        scope_layer = metadata.get("scope_layer", "")
        target_owner = metadata.get("target_owner", "")
        special_owners = {"unresolved", "local-layer"}
        owner_is_path = target_owner not in special_owners and bool(target_owner)
        owner_is_portable = False
        if not target_owner:
            errors.append(f"{record_label} has an empty target_owner")
        elif owner_is_path:
            target = Path(target_owner)
            allowed_owner = (
                target_owner
                in {
                    "README.md",
                    ".codex-plugin/plugin.json",
                    "evolution/README.md",
                    "evolution/candidate-template.md",
                }
                or target_owner.startswith(("skills/", "scripts/", "evals/"))
            )
            owner_is_portable = (
                target != Path(".")
                and not target.is_absolute()
                and ".." not in target.parts
                and "." not in target.parts
                and ":" not in target_owner
                and "\\" not in target_owner
                and bool(re.fullmatch(r"[A-Za-z0-9._/-]+", target_owner))
                and target.suffix in PORTABLE_TEXT_SUFFIXES
                and allowed_owner
            )
            if not owner_is_portable:
                errors.append(f"{record_label} has a non-portable target_owner")
            elif (
                baseline_valid
                and git_available
                and scope_layer != "new-skill"
                and git_text_at(baseline_revision, target_owner) is None
            ):
                errors.append(
                    f"{record_label} target_owner is absent at its baseline"
                )

        if (status == "rejected") != (decision == "reject"):
            errors.append(
                f"{record_label} must pair rejected status with reject decision"
            )
        if decision == "localize" and target_owner != "local-layer":
            errors.append(
                f"{record_label} localize decision requires local-layer owner"
            )
        if target_owner == "local-layer" and decision != "localize":
            errors.append(
                f"{record_label} local-layer owner requires localize decision"
            )
        local_scopes = {
            "task-context",
            "author-profile",
            "project-state",
            "submission-overlay",
        }
        if scope_layer in local_scopes and (
            target_owner != "local-layer" or decision != "localize"
        ):
            errors.append(
                f"{record_label} local scope requires localize and local-layer"
            )
        if target_owner == "local-layer" and scope_layer not in local_scopes:
            errors.append(
                f"{record_label} local-layer owner requires a local scope"
            )
        advanced_statuses = {
            "proposed",
            "authorized",
            "implemented",
            "validated",
            "committed",
        }
        if status in advanced_statuses and not (owner_is_path and owner_is_portable):
            errors.append(
                f"{record_label} advanced status requires a canonical owner path"
            )
        if status in advanced_statuses and decision not in {
            "clarify",
            "correct",
            "extend",
            "deprecate",
        }:
            errors.append(
                f"{record_label} advanced status requires an actionable decision"
            )

        review_after = metadata.get("review_after", "")
        review_date_valid = review_after == "none"
        if not review_date_valid:
            try:
                datetime.strptime(review_after, "%Y-%m-%d")
            except ValueError:
                errors.append(f"{record_label} has an invalid review_after date")
            else:
                review_date_valid = True
        if status in {"deferred", "rework"} and review_after == "none":
            errors.append(f"{record_label} deferred or rework status needs review_after")

        implemented_revision = metadata.get("implemented_revision", "")
        implementation_commit_valid = bool(
            re.fullmatch(r"[0-9a-f]{40}", implemented_revision)
        )
        if implemented_revision != "none" and not implementation_commit_valid:
            errors.append(f"{record_label} has an invalid implemented_revision")
        if status == "committed" and not implementation_commit_valid:
            errors.append(
                f"{record_label} committed status requires implemented_revision"
            )
        if implementation_commit_valid and git_available:
            if not git_object_exists(f"{implemented_revision}^{{commit}}"):
                errors.append(
                    f"{record_label} implemented_revision is not a Git commit"
                )
            elif baseline_valid and (
                implemented_revision == baseline_revision
                or run_git_bytes(
                    "merge-base",
                    "--is-ancestor",
                    baseline_revision,
                    implemented_revision,
                )
                is None
            ):
                errors.append(
                    f"{record_label} implementation does not descend from baseline"
                )
            elif status == "committed" and run_git_bytes(
                "merge-base", "--is-ancestor", implemented_revision, "HEAD"
            ) is None:
                errors.append(
                    f"{record_label} implementation is not in the current source"
                )
            elif owner_is_path and owner_is_portable and git_text_at(
                implemented_revision, target_owner
            ) is None:
                errors.append(
                    f"{record_label} target_owner is absent at implementation"
                )
            elif (
                owner_is_path
                and owner_is_portable
                and baseline_valid
                and git_object_id_at(baseline_revision, target_owner)
                == git_object_id_at(implemented_revision, target_owner)
            ):
                errors.append(
                    f"{record_label} implementation leaves target_owner unchanged"
                )
        if status == "implemented" and implemented_revision == "none":
            current_owner = ROOT / target_owner if owner_is_path else None
            baseline_owner = (
                run_git_bytes("show", f"{baseline_revision}:{target_owner}")
                if baseline_valid and owner_is_path
                else None
            )
            if (
                current_owner is None
                or not owner_is_portable
                or not current_owner.is_file()
            ):
                errors.append(
                    f"{record_label} uncommitted implementation lacks target_owner"
                )
            elif baseline_owner == current_owner.read_bytes():
                errors.append(
                    f"{record_label} uncommitted implementation leaves "
                    "target_owner unchanged"
                )

        validated_snapshot = metadata.get("validated_snapshot", "")
        snapshot_sha = re.fullmatch(r"sha256:([0-9a-f]{64})", validated_snapshot)
        snapshot_commit = re.fullmatch(
            r"commit:([0-9a-f]{40})", validated_snapshot
        )
        snapshot_valid = (
            validated_snapshot == "none"
            or snapshot_sha is not None
            or snapshot_commit is not None
        )
        if not snapshot_valid:
            errors.append(f"{record_label} has an invalid validated_snapshot")
        if status in {"validated", "committed"} and validated_snapshot == "none":
            errors.append(
                f"{record_label} validated or committed status requires an exact "
                "snapshot receipt"
            )
        if snapshot_commit is not None and git_available:
            validated_commit = snapshot_commit.group(1)
            if not git_object_exists(f"{validated_commit}^{{commit}}"):
                errors.append(
                    f"{record_label} validated_snapshot is not a Git commit"
                )
            elif baseline_valid and run_git_bytes(
                "merge-base", "--is-ancestor", baseline_revision, validated_commit
            ) is None:
                errors.append(
                    f"{record_label} validated snapshot does not descend from baseline"
                )
            elif owner_is_path and owner_is_portable and git_text_at(
                validated_commit, target_owner
            ) is None:
                errors.append(
                    f"{record_label} target_owner is absent from validated snapshot"
                )
            elif (
                owner_is_path
                and owner_is_portable
                and baseline_valid
                and git_object_id_at(baseline_revision, target_owner)
                == git_object_id_at(validated_commit, target_owner)
            ):
                errors.append(
                    f"{record_label} validated snapshot leaves target_owner unchanged"
                )
            if status in {"validated", "committed"} and not implementation_commit_valid:
                errors.append(
                    f"{record_label} commit validation requires implemented_revision"
                )
            elif implementation_commit_valid and run_git_bytes(
                "merge-base", "--is-ancestor", implemented_revision, validated_commit
            ) is None:
                errors.append(
                    f"{record_label} validated commit does not descend from "
                    "implemented_revision"
                )
        if snapshot_sha is not None:
            expected_digest = source_snapshot_sha256()
            if snapshot_sha.group(1) != expected_digest:
                errors.append(
                    f"{record_label} SHA-256 receipt does not match current source "
                    "snapshot"
                )
            if owner_is_path and owner_is_portable:
                current_owner = ROOT / target_owner
                baseline_owner = (
                    run_git_bytes("show", f"{baseline_revision}:{target_owner}")
                    if baseline_valid
                    else None
                )
                if not current_owner.is_file():
                    errors.append(
                        f"{record_label} target_owner is absent from current snapshot"
                    )
                elif baseline_owner == current_owner.read_bytes():
                    errors.append(
                        f"{record_label} current snapshot leaves target_owner unchanged"
                    )
            if implementation_commit_valid and run_git_bytes(
                "merge-base", "--is-ancestor", implemented_revision, "HEAD"
            ) is None:
                errors.append(
                    f"{record_label} working snapshot does not descend from "
                    "implemented_revision"
                )
        if status == "committed" and implementation_commit_valid:
            expected_snapshot = f"commit:{implemented_revision}"
            if validated_snapshot != expected_snapshot:
                errors.append(
                    f"{record_label} committed status must validate its exact "
                    "implemented_revision"
                )

        exact_fields = {
            "schema_version": "1",
            "activation": "none",
            "persistence_authorized": "true",
            "visibility": "public-safe",
            "privacy_review": "passed",
        }
        for field, expected in exact_fields.items():
            if metadata.get(field) != expected:
                errors.append(f"{record_label} has an invalid required {field}")

        record_revision = metadata.get("record_revision", "")
        revision_valid = record_revision.isdigit() and int(record_revision) >= 1
        if not revision_valid:
            errors.append(f"{record_label} has an invalid record_revision")

        head_text = git_text_at("HEAD", relative_posix) if git_available else None
        if head_text is None:
            if revision_valid and int(record_revision) != 1:
                errors.append(f"{record_label} new records must use revision 1")
        else:
            previous_errors: list[str] = []
            previous = parse_frontmatter_text(
                head_text, f"committed form of {record_label}", previous_errors
            )
            if previous_errors:
                errors.append(
                    f"{record_label} committed predecessor has invalid frontmatter"
                )
            immutable_fields = {
                "id",
                "created_at",
                "source_skill",
                "source_version",
                "baseline_revision",
            }
            if any(metadata.get(field) != previous.get(field) for field in immutable_fields):
                errors.append(f"{record_label} changes immutable source identity")
            previous_revision = previous.get("record_revision", "")
            previous_revision_valid = previous_revision.isdigit()
            if revision_valid and previous_revision_valid:
                expected_revision = int(previous_revision)
                if text != head_text:
                    expected_revision += 1
                if int(record_revision) != expected_revision:
                    errors.append(
                        f"{record_label} must advance record_revision exactly once"
                    )
            if text != head_text:
                previous_updated_errors: list[str] = []
                previous_updated = parse_utc_timestamp(
                    previous.get("updated_at", ""),
                    "updated_at",
                    f"committed form of {record_label}",
                    previous_updated_errors,
                )
                if previous_updated_errors:
                    errors.append(
                        f"{record_label} committed predecessor has invalid updated_at"
                    )
                elif updated is not None and previous_updated is not None:
                    if updated <= previous_updated:
                        errors.append(
                            f"{record_label} must advance updated_at when changed"
                        )

                previous_status = previous.get("status", "")
                allowed_transitions = CANDIDATE_STATUS_TRANSITIONS.get(
                    previous_status
                )
                if allowed_transitions is None:
                    errors.append(
                        f"{record_label} committed predecessor has invalid status"
                    )
                elif status not in allowed_transitions:
                    errors.append(
                        f"{record_label} uses an invalid lifecycle transition"
                    )

        if SHIPPING_PLACEHOLDER.search(text):
            errors.append(f"{record_label} contains an unresolved placeholder")
        for heading in sorted(CANDIDATE_HEADINGS):
            section = candidate_section_text(text, heading)
            if section is None:
                errors.append(f"{record_label} is missing heading {heading!r}")
                continue
            section = re.sub(r"<!--.*?-->", "", section, flags=re.DOTALL)
            if sum(character.isalnum() for character in section) < 20:
                errors.append(f"{record_label} has an empty or trivial {heading!r}")
        for label, pattern in CANDIDATE_PRIVATE_CONTENT.items():
            if pattern.search(text):
                errors.append(f"{record_label} privacy check found {label}")

    return len(candidate_files)


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
    if sys.argv[1:] == ["--print-source-snapshot"]:
        print(f"sha256:{source_snapshot_sha256()}")
        return 0
    if sys.argv[1:]:
        print("usage: validate_plugin_suite.py [--print-source-snapshot]")
        return 2

    errors: list[str] = []
    validate_manifest(errors)
    skill_names = validate_skills(errors)
    validate_cross_skill_contracts(skill_names, errors)
    validate_reference_structure(errors)
    validate_markdown_links(errors)
    validate_path_portability(errors)
    candidate_count = validate_candidate_ledger(skill_names, errors)
    spec_count = validate_eval_specs(skill_names, errors)

    if errors:
        print("STAR Writing Skills plugin-suite validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "STAR Writing Skills plugin-suite validation passed: "
        f"{len(skill_names)} skills, {spec_count} behavioral specifications "
        f"and {candidate_count} persistent evolution candidates structurally "
        "valid, all local Markdown links resolved, no machine-specific paths "
        "detected. "
        "No behavioral executions were performed."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
