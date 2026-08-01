---
name: star-writing-submit
description: Prepare and audit a research or scholarly manuscript submission against the live requirements of a specific venue, track, year, and submission stage. Use for current author-guideline research, format and anonymity checks, page and font audits, supplementary or code/data packaging, rendered PDF inspection, deadline or post-deadline policy verification, and final submission-readiness reports. Always verify current official sources; never reuse fixed rules from another venue or year.
---

# STAR Writing: Submit

Treat submission requirements as a live, venue-specific overlay on a
substantively stable manuscript. Never encode remembered limits as current
policy.

## Identify the submission target

Record:

- venue and year;
- track or article type;
- initial, revised, camera-ready, artifact, or other stage;
- submission platform;
- deadline, time zone, and modification window;
- manuscript and attachment snapshots.

Do not begin a compliance judgment until these are known. Different tracks or stages may have different rules.

## Retrieve current official requirements

Search current first-party sources:

1. the official submission or author-guideline page;
2. the current author kit, template, or style guide;
3. the official policy, ethics, and FAQ pages;
4. the live submission platform's venue-specific instructions.

Record the source URL, page title, publication or version date when available, and access date. Prefer current, venue-specific instructions over generic platform documentation. When official sources conflict or their precedence is unclear, report the conflict and ask for resolution; do not guess.

Do not rely on:

- remembered rules;
- a previous year's kit;
- another track's instructions;
- third-party summaries;
- an old local template without version confirmation.

If official requirements cannot be accessed, mark the audit incomplete and separate verified facts from assumptions.

## Build a live requirements overlay

Extract only requirements applicable to the identified target:

- page limits and treatment of references or appendices;
- page size, columns, margins, spacing, and font requirements;
- title, author, affiliation, anonymity, and acknowledgment policy;
- abstract, keywords, section, citation, and bibliography rules;
- permitted and prohibited packages, layout changes, or file features;
- figure, table, caption, resolution, accessibility, and color requirements;
- supplementary-material policy;
- code, data, model, artifact, and external-link policy;
- file formats, size limits, naming, number of uploads, and archive structure;
- metadata, conflicts, ethics, disclosure, licensing, and dual-submission rules;
- deadline, grace period, replacement, and post-deadline modification rules.

Create a table with `requirement`, `official source`, `artifact checked`, `status`, and `action`. Keep it outside the permanent general-writing rules because it will expire.

Use [submission-audit.md](references/submission-audit.md) to run the source and package checks.

## Audit source files

Inspect the actual submission source, not only the rendered appearance:

- declared document class and template version;
- packages and manual layout overrides;
- page-breaking, float, spacing, margin, or font modifications;
- author-identifying text, comments, paths, metadata, acknowledgments, and repository links;
- bibliography contents and anonymization behavior;
- embedded or linked figures, tables, appendices, and supplementary references;
- missing files, generated assets, and build dependencies.

Do not remove content or alter scientific claims merely to satisfy layout without explicit authorization. Separate scientific edits from compliance edits.

## Rebuild and inspect the rendered artifact

Build from a clean, reproducible source state when feasible. Capture the command, engine, template, and log.

Check:

- successful compilation and unresolved references or citations;
- page count and page dimensions;
- body, table, caption, footnote, and figure-text fonts;
- font embedding and prohibited font types when specified;
- margins, columns, line spacing, floats, and overflow;
- raster resolution and vector-font behavior;
- figure and table legibility at final size;
- color, grayscale, and color-vision accessibility where required;
- hidden metadata, links, annotations, comments, or identifying information;
- final file size and opening/rendering in an independent viewer.

Inspect the PDF visually page by page. A clean compilation log does not prove visual or policy compliance.

Treat rendered-artifact checks as hash-bound. Any recompilation, figure
regeneration, export, compression, metadata rewrite, or package rebuild
invalidates checks that depend on the previous binary. Re-run the affected
checks on the exact file intended for upload. Diagnose embedded object sizes
before compressing globally; preserve vector content and downsample only raster
assets that materially affect the limit when the venue permits it.

When Poppler utilities are available, use
[inspect_pdf.py](../../scripts/inspect_pdf.py) to record the hash, size, page
geometry, font state, raster resolution, and largest embedded raster objects.
Pass only thresholds verified for the current venue; the script reports facts
and does not supply policy.

## Audit anonymity

Apply the venue's exact anonymity policy. Check:

- author names, affiliations, acknowledgments, contribution statements, and biographies;
- self-citations and self-referential wording;
- repository, dataset, demo, project, and supplementary links;
- filenames, PDF metadata, archive paths, comments, and embedded document properties;
- funding, ethics, institutional, or location details;
- code or data contents that reveal identity.

Do not over-anonymize when the official policy requires normal citation of prior work. Record uncertain cases for human decision.

## Audit supplementary, code, and data packages

Follow the live policy for what may or must be uploaded. Never assume an archive type, size limit, or external-hosting rule.

Check:

- allowed format and size;
- anonymization;
- completeness of source, configuration, environment, preprocessing, evaluation, and artifact provenance;
- availability or generation route for data;
- licenses and redistribution permission;
- executable entry points and minimal instructions;
- absence of secrets, credentials, personal data, absolute private paths, caches, or unrelated large files;
- consistency with reproducibility statements in the manuscript;
- archive extraction and basic use in a clean location.

Distinguish arithmetic reproduction, figure regeneration, checkpoint evaluation, and end-to-end reproduction. Do not describe one as another.

For every code, data, model, or supplementary artifact, distinguish:

- currently provided or publicly accessible;
- included with the present submission;
- committed for release upon acceptance;
- planned for release after publication;
- unavailable.

Verify current availability from the actual package or access route. Make the
checklist, Data Availability statement, archive README, and submission metadata
use the same status and tense. Never rewrite a future commitment as current
availability.

## Respect external-action boundaries

Treat upload, replacement, author-list changes, conflict declarations, and final submission as external state changes. Audit and prepare files without submitting them unless the user explicitly authorizes the exact action and target.

Before any authorized upload:

1. show the exact files and hashes;
2. show unresolved warnings;
3. confirm the venue, track, stage, and deadline;
4. preserve a local copy of the submitted artifacts.

Do not call an artifact ready when its recorded hash differs from the file
currently present at the upload path.

## Deliver a submission-readiness report

Report:

1. target venue, track, stage, and audited snapshot;
2. official sources with access dates;
3. compliant items;
4. violations and risks ranked by severity;
5. uncertain or conflicting requirements;
6. rendered-artifact findings;
7. anonymity findings;
8. attachment and package findings;
9. exact changes required before submission;
10. files, hashes, and remaining blockers.

State explicitly whether the audit is complete. Do not say “submission-ready” while any mandatory rule remains unverified.
