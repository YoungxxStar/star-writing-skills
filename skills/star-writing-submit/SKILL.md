---
name: star-writing-submit
description: Prepare and audit research-paper submissions and associated artifacts against live requirements from a venue, publisher, repository, or submission platform. Use for current rule research, format and anonymity checks, rendered or form-based inspection, supplement or code/data packaging, deadline and modification policy, and readiness reports across journals, conferences, and workshops. Apply only relevant checks and never reuse rules from another target or cycle.
---

# STAR Writing: Submit

Treat submission requirements as a live, target-specific overlay on a
substantively stable artifact. Never encode remembered limits as current policy.

## Identify the submission target

Record:

- governing authority or destination;
- rule-set cycle, version, or effective date;
- paper category, track, or article type;
- initial, revised, camera-ready, final, response, deposit, or other publication
  stage;
- submission channel or delivery mechanism, when one exists;
- deadline, time zone, and modification window, when applicable;
- primary and supporting artifact snapshots.

Do not begin a compliance judgment until the applicable target coordinates are
known. Mark a coordinate `not applicable` rather than inventing a venue, year,
track, deadline, platform, or upload.

## Retrieve current official requirements

Search current first-party sources:

1. the current call for papers, submission, deposit, or author-guideline page;
2. the current template, style guide, or form specification;
3. the applicable policy, ethics, disclosure, and FAQ pages;
4. the live platform or delivery-channel instructions, when applicable.

Record the source URL, title, publication or version date when available, and
access date. Prefer current target-specific instructions over generic platform
documentation. When official sources conflict or their precedence is unclear,
report the conflict and ask for resolution; do not guess.

Do not rely on:

- remembered rules;
- a previous cycle's rules;
- another category's instructions;
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

Apply an explicit applicability gate to every branch below. Mark unsupported
branches `not applicable`; do not create a PDF, anonymity requirement,
supplement, package, repository release, or upload workflow merely because the
skill can inspect one.

Use [submission-audit.md](references/submission-audit.md) to run the source and package checks.

## Audit source files when delivered

When editable source or a source bundle is part of the target, inspect the
actual delivered source, not only the rendered appearance:

- declared document class and template version;
- packages and manual layout overrides;
- page-breaking, float, spacing, margin, or font modifications;
- author-identifying text, comments, paths, metadata, acknowledgments, and repository links;
- bibliography contents and anonymization behavior;
- embedded or linked figures, tables, appendices, and supplementary references;
- missing files, generated assets, and build dependencies.

Do not remove content or alter scientific claims merely to satisfy layout without explicit authorization. Separate scientific edits from compliance edits.

## Inspect a rendered artifact when required

When the target requires a rendered or fixed-layout artifact, build or export
from a clean, reproducible source state when feasible. Capture the command,
engine or application, template, export settings, and log.

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

For a PDF, inspect it visually page by page. For DOCX, slides, web-form export,
or another format, inspect the corresponding final representation. A clean
build or export log does not prove visual or policy compliance.

Treat rendered-artifact checks as hash-bound. Any recompilation, figure
regeneration, export, compression, metadata rewrite, or package rebuild
invalidates checks that depend on the previous binary. Re-run the affected
checks on the exact file intended for upload. Diagnose embedded object sizes
before compressing globally; preserve vector content and downsample only raster
assets that materially affect the limit when the governing requirements permit
it.

When Poppler utilities are available, use
[inspect_pdf.py](../../scripts/inspect_pdf.py) to record the hash, size, page
geometry, font state, raster resolution, and largest embedded raster objects.
Pass only thresholds verified for the current target; the script reports facts
and does not supply policy.

## Audit identity requirements when applicable

Apply the governing authority's exact anonymity, attribution, or identity
policy. Check only the applicable fields:

- author names, affiliations, acknowledgments, contribution statements, and biographies;
- self-citations and self-referential wording;
- repository, dataset, demo, project, and supplementary links;
- filenames, PDF metadata, archive paths, comments, and embedded document properties;
- funding, ethics, affiliation, or location details;
- code or data contents that reveal identity.

Do not remove required attribution merely because another target uses anonymous
review. Record uncertain cases for human decision.

## Audit supporting packages when applicable

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

Treat upload, delivery, replacement, deposit, identity changes, declarations, and
final submission as external state changes. Audit and prepare artifacts without
sending them unless the user explicitly authorizes the exact action and target.

Before any authorized upload:

1. show the exact files and hashes;
2. show unresolved warnings;
3. confirm the governing authority, paper category, stage, and any deadline;
4. preserve a local copy of the submitted artifacts.

Do not call an artifact ready when its recorded hash differs from the file
currently present at the upload path.

## Deliver a submission-readiness report

For any authorized correction, explain each substantive item with
[the highlighted `LIVE-REQUIREMENTS` or `SEMANTIC-PRESERVATION` tag](../star-writing/references/principle-tags.md)
and cite the verified live rule or artifact finding separately. Keep these tags
out of the submitted artifacts.

Report:

1. governing authority, paper category, stage, and audited snapshot;
2. official sources with access dates;
3. compliant items;
4. violations and risks ranked by severity;
5. uncertain or conflicting requirements;
6. applicable rendered- or form-artifact findings;
7. applicable identity or anonymity findings;
8. applicable attachment and package findings;
9. exact changes required before submission;
10. files, hashes, and remaining blockers.

State explicitly whether the audit is complete. Do not say “submission-ready” while any mandatory rule remains unverified.
