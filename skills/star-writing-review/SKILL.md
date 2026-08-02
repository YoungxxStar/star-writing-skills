---
name: star-writing-review
description: Perform a purpose-specific, evidence-grounded review of research papers and associated rebuttals or supplements. Use for reviewer simulation, adversarial stress tests, whole-paper or cross-section consistency audits, rebuttal assessment, feedback triage, or submission-readiness judgment across fields and venues. Separate applicable dimensions such as novelty, validity, mechanism, utility, reproducibility, responsiveness, and presentation. Default to read-only review unless edits are explicitly requested.
---

# STAR Writing: Review

Review the strongest defensible version of the paper, then stress-test it. Do not reward ambitious wording that the evidence cannot support, and do not demand work unrelated to the paper's actual claim.

Do not load the
[shared evolution policy](../star-writing/references/evolution-policy.md) for
ordinary paper work. If the user explicitly asks the plugin to learn, or this
task exposes a material, plausibly reusable success, correction, or gap, keep
this skill responsible for the paper, retain only a task-local candidate, and route plugin
maintenance to `star-writing-evolve`. Feedback alone cannot authorize a source
change.

## Set the mode

- Use **audit** for reviewer simulation, whole-manuscript judgment, consistency
  review, rejection-risk analysis, and feedback triage.
- Review is read-only. Proposed corrections do not authorize manuscript edits;
  route an accepted scientific revision to `star-writing-draft` and a
  wording-only revision to `star-writing-polish`.

## Preserve review scope

1. Identify the exact paper snapshot and any included supplement, rebuttal, or
   other publication artifact.
2. Record the review purpose, requested scope, decision to be supported, and any
   sources available for verification.
3. Default to read-only analysis. Do not edit manuscript, code, figures, references, or submission files unless explicitly asked.
4. Separate verified problems from suspicions and unavailable evidence.
5. Avoid evaluating a stale draft when concurrent edits exist; anchor findings to locations or a version.

## Reconstruct before judging

For a paper or paper-wide review, write a compact reconstruction:

- the research question;
- the central claim;
- the closest alternative or prior approach;
- the proposed insight or intervention;
- the decisive evidence;
- the claimed scope and limitations.

For a rebuttal or response review, instead reconstruct the disputed claim, the
comment's factual premise, the proposed response, its supporting evidence, the
corresponding manuscript change, and any unresolved risk.

If the applicable reconstruction cannot be made consistently, report the
contract or traceability problem before line-editing prose.

## Run an adversarial rejection-case analysis

For a consequential reviewer simulation, rejection-risk analysis, or disputed
central contribution, steelman the paper before attacking it. Reduce the
contribution to plain operations, construct the strongest plausible rejection
case, answer it with the strongest evidence-grounded author response, and then
adjudicate. Read
[adversarial-review.md](references/adversarial-review.md) for the complete
workflow.

Do not confuse skepticism with accuracy. Apply the same evidential standard in
both directions, report an objection as unsupported when its premise is false,
and do not weaken a directly established result merely to sound cautious.

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

Do not collapse all merit into one judgment. Select only dimensions relevant to
the review purpose and mark the rest `not applicable` rather than inventing a
defect or obligation.

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

### Responsiveness

For rebuttals and revisions, ask whether every material comment is answered at
the level of its verified premise, whether the response is supported, and
whether each claimed change can be traced to the current paper. Do not reward a
polished answer that evades the underlying issue.

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

For each central result or argument in the paper, identify the strongest
plausible rival explanation. Determine whether the design or reasoning controls
it, measures it, argues it away, or leaves it unresolved. In a rebuttal-only
audit, apply this test to the disputed claim rather than manufacturing a new
paper-wide objection.

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

Load the
[project terminology and symbol ledger](../star-writing/references/terminology-and-symbols.md)
when it exists; otherwise build a short list of canonical objects, terms,
symbols, metrics, populations, and result values. Check them across the units
that actually exist:

- title and abstract;
- introduction and contributions;
- related work;
- methods and equations;
- experimental or study setup;
- results and discussion;
- figures, tables, and captions;
- limitations and conclusion;
- supplementary material;
- rebuttal, response, or revision letter, when included.

Apply the propagation rule: when a definition, assumption, metric, claim, or result changes, inspect every downstream use. Do not mechanically replace words when two similar terms refer to genuinely different objects.

## Prove audit completeness

When the user requests a full, final, or exhaustive review, traverse the
artifact in document order rather than relying on searches and global scans.
Review every applicable section, paragraph, sentence, equation, table, figure,
caption, and reference. Record each unit as checked, revised, retained with
reason, unverified, or not applicable. Search and linting remain useful for
cross-document patterns, but they do not establish that every unit was read.

For long artifacts, keep a compact section-level coverage summary and record
findings, unresolved units, retained exceptions, and changed dependencies
individually. Keep the ledger task-local unless persistence is authorized, and
do not dump a sentence-by-sentence list merely to signal thoroughness.

For every retained unit, ask what reader, inferential, evidential, technical,
or reproduction role it performs. Recommend removal when a correct unit has no
necessary role. Verify, narrow, or omit low-confidence detail instead of
repairing it through more elaborate prose.

Classify each claim-bearing sentence by support and assess each paragraph at
its weakest load-bearing statement. Do not hide a central unknown by averaging
it with several high-confidence sentences.

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

Match the opening to the review purpose:

- For reviewer simulation or rejection-risk analysis, lead with the strongest
  defensible contribution, strongest plausible rejection case, best
  evidence-grounded response, surviving vulnerability, and conditional verdict.
- For a consistency, completeness, or focused audit, lead with the audited
  boundary, overall finding, and highest-priority verified problems. Do not force
  a rejection narrative.
- For a rebuttal or revision audit, lead with response coverage, unsupported or
  unresolved answers, manuscript-change traceability, and remaining decision
  risk.

Then report findings by severity. For every finding include:

- location;
- current claim or problem;
- evidence for the finding;
- why it matters;
- required action;
- whether wording alone can fix it.

When a finding proposes a substantive target-artifact change, label that action with
[one highlighted governing principle](../star-writing/references/principle-tags.md)
and give the evidence for the finding separately. Do not tag a research gap as
if wording could resolve it, and do not copy tags into proposed artifact text.

Finish with:

- a propagation checklist for accepted changes;
- claims that should be narrowed or removed;
- evidence that remains unverified;
- optional improvements clearly separated from required corrections.

State the traversal boundary and any unit class not checked. Do not report a
full audit when only selected sections, search hits, or compilation diagnostics
were inspected.

Do not silently rewrite the manuscript. If the user later requests edits, preserve the scientific scope established by the review and report every material claim change.
