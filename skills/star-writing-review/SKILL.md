---
name: star-writing-review
description: Perform a skeptical, evidence-grounded review of research and scholarly manuscripts that separates novelty, validity, mechanism, utility, reproducibility, and presentation; tests the central argument against strong alternatives; audits citations, definitions, and global consistency; and reports findings by severity. Use for pre-submission review, reviewer simulation, whole-manuscript audits, section-to-section consistency checks, triaging reviewer, collaborator, editor, or agent feedback, or diagnosing what must change before polishing. Default to read-only review unless the user explicitly requests edits.
---

# STAR Writing: Review

Review the strongest defensible version of the paper, then stress-test it. Do not reward ambitious wording that the evidence cannot support, and do not demand work unrelated to the paper's actual claim.

## Preserve review scope

1. Identify the exact manuscript snapshot and included supplementary material.
2. Record the requested review scope and any sources available for verification.
3. Default to read-only analysis. Do not edit manuscript, code, figures, references, or submission files unless explicitly asked.
4. Separate verified problems from suspicions and unavailable evidence.
5. Avoid evaluating a stale draft when concurrent edits exist; anchor findings to locations or a version.

## Reconstruct before judging

Write a compact reconstruction:

- the research question;
- the central claim;
- the closest alternative or prior approach;
- the proposed insight or intervention;
- the decisive evidence;
- the claimed scope and limitations.

If this reconstruction cannot be made consistently from the manuscript, report an argument-structure problem before line-editing prose.

## Triage external feedback before acting

Treat reviewer, collaborator, editor, and agent comments as hypotheses, not
instructions whose premises are already true. For each material comment,
separate:

- the factual premise;
- the scientific or evidential risk;
- the requested evidence or analysis;
- the prose or presentation preference;
- the venue or policy judgment.

Verify each premise against its responsible source, then assign `accept`,
`partially accept`, `reject`, or `unresolved`. Preserve a useful correction even
when the comment's rationale is wrong, and reject an unsupported request even
when it sounds authoritative. Do not implement feedback that depends on
uninspected code, data, analysis, primary literature, or current policy.

## Audit distinct dimensions

Do not collapse all merit into one judgment.

### Novelty

Ask what is new relative to the closest work, not merely whether the components sound unusual. Compare problem definition, available information, outputs, assumptions, mechanism, and evidence scope. Verify decisive literature claims at the proposition level.

### Validity

Ask whether definitions, methods, data, analyses, statistics, and conclusions are internally sound. Check that results are calculated from the stated population and protocol.

### Mechanism

Ask whether the evidence identifies why the effect occurred. Distinguish controlled mechanism evidence from a plausible explanation of a whole-system difference.

### Utility

Ask whether practical or downstream value was directly evaluated. Treat untested applications as prospective motivation, not demonstrated benefit.

### Reproducibility

Ask whether another qualified researcher could reconstruct the study's inputs, procedure, environment, analysis, and reported outputs from the available artifacts and documentation.

### Presentation

Ask whether the reader can follow the argument without guessing definitions, comparison conditions, evidence roles, or statistical meaning. Treat presentation as distinct from scientific validity.

Read [skeptical-review-rubric.md](references/skeptical-review-rubric.md) for
detailed prompts when performing a full review or triaging a substantial set of
external comments.

## Trace claims and evidence in both directions

For every central claim, locate its direct evidence and inference. For every major figure, table, theorem, or study, identify which claim it supports.

Flag:

- claims without evidence;
- evidence without an argumentative role;
- conclusions stronger than their originating results;
- duplicated evidence that consumes space without increasing identification;
- essential support hidden outside the main argument.

## Challenge alternative explanations

For each central result, identify the strongest plausible rival explanation. Determine whether the design controls it, measures it, argues it away, or leaves it unresolved.

When recommending additional evidence, state:

1. the exact uncertainty or rival explanation;
2. why it threatens a material claim;
3. the smallest analysis, control, derivation, or revision that would address it.

Do not request generic extra experiments.

## Audit citations

Check whether each important citation supports the exact clause in which it appears. Distinguish:

- original source from secondary summary;
- method from application pipeline;
- input, output, and assumptions;
- publication status;
- what the source explicitly establishes from what the manuscript infers.

When verification is incomplete, mark the citation as unverified rather than declaring it correct.

## Audit definitions and global consistency

Build a short list of canonical objects, terms, symbols, metrics, populations, and result values. Check them across:

- title and abstract;
- introduction and contributions;
- related work;
- methods and equations;
- experimental or study setup;
- results and discussion;
- figures, tables, and captions;
- limitations and conclusion;
- supplementary material.

Apply the propagation rule: when a definition, assumption, metric, claim, or result changes, inspect every downstream use. Do not mechanically replace words when two similar terms refer to genuinely different objects.

## Prove audit completeness

When the user requests a full, final, or exhaustive review, traverse the
artifact in document order rather than relying on searches and global scans.
Review every applicable section, paragraph, sentence, equation, table, figure,
caption, and reference. Record each unit as verified, revised, retained with
reason, unverified, or not applicable. Search and linting remain useful for
cross-document patterns, but they do not establish that every unit was read.

For every retained unit, ask what reader, inferential, evidential, technical,
or reproduction role it performs. Recommend removal when a correct unit has no
necessary role. Verify, narrow, or omit low-confidence detail instead of
repairing it through more elaborate prose.

## Review the reader's path

At each section, ask:

- Has the required concept already been defined?
- Is the purpose of this paragraph clear?
- Does the evidence appear close enough to the claim it supports?
- Does the transition encode a real logical relation?
- Is a figure or table placed according to argumentative dependency rather than empty space?

Diagnose structural problems before sentence-level style.

## Classify findings by severity

Use:

- **Critical** — invalidates or materially contradicts a central claim, study design, evidence source, or required ethical condition.
- **Major** — threatens a main contribution, comparison, interpretation, or reproducibility claim and requires substantive correction.
- **Moderate** — materially weakens clarity, scope, or evidential transparency but does not overturn the central result.
- **Minor** — local wording, notation, citation formatting, or presentation issue with limited scientific effect.

Do not inflate severity to make the review appear rigorous. Distinguish:

- missing reporting;
- missing evidence;
- invalid design;
- unsupported interpretation;
- terminology or presentation error.

## Deliver a decision-useful report

Lead with:

1. the strongest defensible contribution;
2. the central vulnerability;
3. an overall readiness judgment with its conditions.

Then report findings by severity. For every finding include:

- location;
- current claim or problem;
- evidence for the finding;
- why it matters;
- required action;
- whether wording alone can fix it.

Finish with:

- a propagation checklist for accepted changes;
- claims that should be narrowed or removed;
- evidence that remains unverified;
- optional improvements clearly separated from required corrections.

State the traversal boundary and any unit class not checked. Do not report a
full audit when only selected sections, search hits, or compilation diagnostics
were inspected.

Do not silently rewrite the manuscript. If the user later requests edits, preserve the scientific scope established by the review and report every material claim change.
